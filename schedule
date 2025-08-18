import sql from "@/app/api/utils/sql";

// Handle appointment scheduling during calls
export async function POST(request) {
  try {
    const formData = await request.formData();
    const speechResult = formData.get("SpeechResult") || "";
    const digits = formData.get("Digits") || "";
    const from = formData.get("From") || "";
    const { searchParams } = new URL(request.url);
    const campaignId = searchParams.get("campaign_id");
    const testCall = searchParams.get("test_call") === "true";

    // Determine scheduling preference
    const userInput = speechResult || digits;
    let schedulingWeek = "this";
    let response = "";

    if (userInput.toLowerCase().includes("next week") || digits === "2") {
      schedulingWeek = "next";
      response = "Perfect! I'll schedule an appointment for next week.";
    } else if (
      userInput.toLowerCase().includes("this week") ||
      digits === "1"
    ) {
      schedulingWeek = "this";
      response = "Excellent! I'll schedule an appointment for this week.";
    } else {
      // Default to this week if unclear
      response = "Great! I'll schedule an appointment for this week.";
    }

    // Create appointment record
    try {
      const customerName = testCall ? "Test User" : "Prospective Customer";

      // Calculate appointment date
      const appointmentDate = new Date();
      if (schedulingWeek === "next") {
        appointmentDate.setDate(
          appointmentDate.getDate() + 7 + Math.floor(Math.random() * 5),
        ); // Next week + 0-4 days
      } else {
        appointmentDate.setDate(
          appointmentDate.getDate() + 1 + Math.floor(Math.random() * 4),
        ); // 1-4 days from now
      }
      appointmentDate.setHours(9 + Math.floor(Math.random() * 8), 0, 0, 0); // 9 AM to 5 PM

      // Get available agent
      const agents =
        await sql`SELECT name FROM agents WHERE active = true ORDER BY RANDOM() LIMIT 1`;
      const agentName = agents[0]?.name || "Available Agent";

      const notes = testCall
        ? `[TEST CALL] Scheduled via Agent Brian - ${schedulingWeek} week preference`
        : `Scheduled via Agent Brian - ${schedulingWeek} week preference`;

      await sql`
        INSERT INTO appointments (campaign_id, customer_name, phone, scheduled_for, agent_name, status, notes)
        VALUES (${campaignId}, ${customerName}, ${from}, ${appointmentDate.toISOString()}, ${agentName}, 'pending', ${notes})
      `;

      // Update campaign appointment count (only for non-test calls)
      if (!testCall) {
        await sql`
          UPDATE campaigns 
          SET appointments_booked = appointments_booked + 1,
              updated_at = CURRENT_TIMESTAMP
          WHERE id = ${campaignId}
        `;
      }

      // Format date for speaking
      const dayName = appointmentDate.toLocaleDateString("en-US", {
        weekday: "long",
      });
      const timeString = appointmentDate.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      });

      response += ` Our agent ${agentName} will call you on ${dayName} at ${timeString}. Thank you for your interest!`;
    } catch (dbError) {
      console.error("Error creating appointment:", dbError);
      response =
        "I've noted your interest and someone from our team will contact you soon to schedule an appointment.";
    }

    const twiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="man" language="en-US">
    ${escapeXml(response)}
  </Say>
  <Say voice="man" language="en-US">
    Have a wonderful day!
  </Say>
  <Hangup/>
</Response>`;

    return new Response(twiml, {
      status: 200,
      headers: {
        "Content-Type": "text/xml",
      },
    });
  } catch (error) {
    console.error("Error in scheduling flow:", error);

    const errorTwiml = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="man" language="en-US">
    This is Agent Brian. Thank you for your interest. Someone from our team will contact you soon to schedule an appointment.
  </Say>
  <Say voice="man" language="en-US">
    Have a wonderful day!
  </Say>
  <Hangup/>
</Response>`;

    return new Response(errorTwiml, {
      status: 200,
      headers: {
        "Content-Type": "text/xml",
      },
    });
  }
}

// Helper function to escape XML characters
function escapeXml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}
