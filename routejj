import sql from "@/app/api/utils/sql";

// Make actual AI calling bot calls using Twilio
export async function POST(request) {
  try {
    const body = await request.json();
    const {
      campaign_id,
      phone_numbers,
      test_call = false,
      demo_mode = false,
    } = body;

    if (!campaign_id || !phone_numbers || !Array.isArray(phone_numbers)) {
      return Response.json(
        {
          error: "Campaign ID and phone numbers array are required",
        },
        { status: 400 },
      );
    }

    // Get campaign details
    const [campaign] = await sql`
      SELECT * FROM campaigns WHERE id = ${campaign_id}
    `;

    if (!campaign) {
      return Response.json({ error: "Campaign not found" }, { status: 404 });
    }

    // Demo mode - simulate calls without Twilio
    if (demo_mode) {
      const callResults = [];
      let appointmentsScheduled = 0;

      for (const phone of phone_numbers) {
        // Simulate realistic call outcomes
        const outcomes = [
          {
            status: "answered",
            duration: Math.floor(Math.random() * 180) + 30,
            appointment: Math.random() > 0.7,
          },
          { status: "busy", duration: 0, appointment: false },
          { status: "no-answer", duration: 0, appointment: false },
          {
            status: "answered",
            duration: Math.floor(Math.random() * 120) + 20,
            appointment: Math.random() > 0.6,
          },
        ];

        const outcome = outcomes[Math.floor(Math.random() * outcomes.length)];
        const scheduledAppointment = outcome.appointment;

        if (scheduledAppointment) {
          appointmentsScheduled++;

          // Create a simulated appointment
          const scheduledFor = new Date();
          scheduledFor.setDate(
            scheduledFor.getDate() + Math.floor(Math.random() * 7) + 1,
          ); // 1-7 days from now
          scheduledFor.setHours(Math.floor(Math.random() * 8) + 9); // 9 AM to 5 PM
          scheduledFor.setMinutes(0);

          const customerName = "Demo Customer " + phone.slice(-4);
          const appointmentNotes = "[DEMO] Simulated appointment scheduled";

          await sql`
            INSERT INTO appointments (campaign_id, customer_name, phone, scheduled_for, agent_name, status, notes)
            VALUES (${campaign_id}, ${customerName}, ${phone}, ${scheduledFor}, 'Agent Brian', 'pending', ${appointmentNotes})
          `;
        }

        // Log the simulated call
        const callNotes = "[DEMO] Simulated call - Agent Brian";
        await sql`
          INSERT INTO call_logs (campaign_id, phone, call_status, call_duration, appointment_scheduled, notes)
          VALUES (${campaign_id}, ${phone}, ${outcome.status}, ${outcome.duration}, ${scheduledAppointment}, ${callNotes})
        `;

        callResults.push({
          phone,
          status: outcome.status,
          duration: outcome.duration,
          appointmentScheduled: scheduledAppointment,
          customerName: scheduledAppointment
            ? `Demo Customer ${phone.slice(-4)}`
            : null,
          scheduledFor: scheduledAppointment
            ? new Date(Date.now() + Math.random() * 7 * 24 * 60 * 60 * 1000)
            : null,
          notes: `[DEMO] Agent Brian - ${outcome.status}`,
          isTestCall: false,
          isDemoCall: true,
          twilioCallSid: "demo_" + Math.random().toString(36).substr(2, 9),
        });

        // Small delay to simulate realistic timing
        await new Promise((resolve) => setTimeout(resolve, 500));
      }

      // Update campaign stats
      await sql`
        UPDATE campaigns 
        SET calls_made = calls_made + ${phone_numbers.length},
            appointments_booked = appointments_booked + ${appointmentsScheduled},
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ${campaign_id}
      `;

      return Response.json({
        campaign_id,
        total_calls: phone_numbers.length,
        appointments_scheduled: appointmentsScheduled,
        call_results: callResults,
        is_demo_mode: true,
        message:
          "Demo calls completed successfully! Agent Brian simulated realistic call outcomes.",
        note: "This was a simulated demo - no actual calls were made.",
      });
    }

    // Check for required Twilio credentials for real calls
    const twilioAccountSid = process.env.TWILIO_ACCOUNT_SID;
    const twilioAuthToken = process.env.TWILIO_AUTH_TOKEN;
    const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;

    if (!twilioAccountSid || !twilioAuthToken || !twilioPhoneNumber) {
      return Response.json(
        {
          error:
            "Twilio credentials not configured. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER environment variables, or use demo_mode: true for testing.",
          demo_suggestion:
            "Add 'demo_mode': true to your request to test without Twilio credentials.",
        },
        { status: 500 },
      );
    }

    // Rest of the existing Twilio code for real calls...
    const callResults = [];
    let appointmentsScheduled = 0;

    // Make actual calls using Twilio
    for (const phone of phone_numbers) {
      try {
        // Create TwiML for the call
        const script =
          campaign.script || "Hello, this is a call from our automated system.";
        const twimlUrl = `${process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"}/api/call-bot/twiml?campaign_id=${campaign_id}&test_call=${test_call}&script=${encodeURIComponent(script)}`;

        // Make the call using Twilio REST API
        const callResponse = await fetch(
          `https://api.twilio.com/2010-04-01/Accounts/${twilioAccountSid}/Calls.json`,
          {
            method: "POST",
            headers: {
              Authorization: `Basic ${Buffer.from(`${twilioAccountSid}:${twilioAuthToken}`).toString("base64")}`,
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
              To: phone,
              From: twilioPhoneNumber,
              Url: twimlUrl,
              StatusCallback: `${process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"}/api/call-bot/webhook`,
              StatusCallbackEvent: "completed,failed,busy,no-answer",
              Record: "true", // Record calls for quality monitoring
              RecordingStatusCallback: `${process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"}/api/call-bot/recording-webhook`,
            }),
          },
        );

        if (!callResponse.ok) {
          const errorData = await callResponse.text();
          console.error(`Twilio API error for ${phone}:`, errorData);

          // Log failed call
          const failedCallNotes =
            (test_call ? "[TEST CALL] " : "") +
            "Failed to initiate call: " +
            errorData;
          await sql`
            INSERT INTO call_logs (campaign_id, phone, call_status, call_duration, appointment_scheduled, notes)
            VALUES (${campaign_id}, ${phone}, 'failed', 0, false, ${failedCallNotes})
          `;

          callResults.push({
            phone,
            status: "failed",
            duration: 0,
            appointmentScheduled: false,
            customerName: null,
            scheduledFor: null,
            notes: `${test_call ? "[TEST CALL] " : ""}Failed to initiate call`,
            isTestCall: test_call,
            twilioCallSid: null,
          });
          continue;
        }

        const callData = await callResponse.json();

        // Log initiated call
        const initiatedCallNotes =
          (test_call ? "[TEST CALL] " : "") +
          "Call initiated with SID: " +
          callData.sid;
        await sql`
          INSERT INTO call_logs (campaign_id, phone, call_status, call_duration, appointment_scheduled, notes)
          VALUES (${campaign_id}, ${phone}, 'initiated', 0, false, ${initiatedCallNotes})
        `;

        callResults.push({
          phone,
          status: "initiated",
          duration: 0,
          appointmentScheduled: false,
          customerName: null,
          scheduledFor: null,
          notes: `${test_call ? "[TEST CALL] " : ""}Call initiated`,
          isTestCall: test_call,
          twilioCallSid: callData.sid,
        });

        // Small delay between calls to avoid rate limiting
        await new Promise((resolve) => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(`Error making call to ${phone}:`, error);

        // Log error
        const errorNotes =
          (test_call ? "[TEST CALL] " : "") + "Error: " + error.message;
        await sql`
          INSERT INTO call_logs (campaign_id, phone, call_status, call_duration, appointment_scheduled, notes)
          VALUES (${campaign_id}, ${phone}, 'error', 0, false, ${errorNotes})
        `;

        callResults.push({
          phone,
          status: "error",
          duration: 0,
          appointmentScheduled: false,
          customerName: null,
          scheduledFor: null,
          notes: `${test_call ? "[TEST CALL] " : ""}Error: ${error.message}`,
          isTestCall: test_call,
          twilioCallSid: null,
        });
      }
    }

    // Update campaign stats (only for non-test calls)
    if (!test_call) {
      await sql`
        UPDATE campaigns 
        SET calls_made = calls_made + ${phone_numbers.length},
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ${campaign_id}
      `;
    }

    return Response.json({
      campaign_id,
      total_calls: phone_numbers.length,
      appointments_scheduled: appointmentsScheduled, // Will be updated via webhooks
      call_results: callResults,
      is_test_call: test_call,
      message:
        "Calls initiated successfully. Results will be updated as calls complete.",
      webhook_note:
        "Call outcomes and appointments will be processed via Twilio webhooks.",
    });
  } catch (error) {
    console.error("Error initiating calls:", error);
    return Response.json(
      { error: "Failed to initiate calls: " + error.message },
      { status: 500 },
    );
  }
}
