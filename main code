"use client";

import { useState } from "react";
import { useDashboard } from "../hooks/useDashboard";
import Header from "../components/Layout/Header";
import Sidebar from "../components/Layout/Sidebar";
import StatsCards from "../components/Dashboard/StatsCards";
import CampaignList from "../components/Dashboard/Campaigns/CampaignList";
import AppointmentList from "../components/Dashboard/Appointments/AppointmentList";
import NewCampaignModal from "../components/Dashboard/Modals/NewCampaignModal";
import CallNumbersModal from "../components/Dashboard/Modals/CallNumbersModal";
import TestCallModal from "../components/Dashboard/Modals/TestCallModal";
import FeedbackModal from "../components/Dashboard/Modals/FeedbackModal";
import LoadingSpinner from "../components/UI/LoadingSpinner";
import ErrorNotification from "../components/UI/ErrorNotification";
import SetupStatus from "../components/Dashboard/SetupStatus";

export default function DashboardPage() {
  const {
    stats,
    activeCampaigns,
    recentAppointments,
    isLoading,
    isActionLoading,
    error,
    lastTestCallResult,
    setupStatus,
    setError,
    toggleCampaign,
    deleteCampaign,
    cancelAppointment,
    createCampaign,
    callSpecificNumbers,
    testCallMe,
    submitFeedback,
    clearLastTestCallResult,
    checkEnvironmentSetup,
  } = useDashboard();

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [showNewCampaignModal, setShowNewCampaignModal] = useState(false);
  const [showCallNumbersModal, setShowCallNumbersModal] = useState(false);
  const [showTestCallModal, setShowTestCallModal] = useState(false);
  const [showFeedbackModal, setShowFeedbackModal] = useState(false);

  const handleCreateCampaign = async (campaignData) => {
    const success = await createCampaign(campaignData);
    if (success) {
      setShowNewCampaignModal(false);
    }
  };

  const handleCallNumbers = async (callData) => {
    const success = await callSpecificNumbers(callData);
    if (success) {
      setShowCallNumbersModal(false);
    }
  };

  const handleTestCall = async (testData) => {
    const success = await testCallMe(testData);
    if (success) {
      setShowTestCallModal(false);
      // Show feedback modal after a delay to allow user to answer the call
      setTimeout(() => {
        setShowFeedbackModal(true);
      }, 2000);
    }
  };

  const handleSubmitFeedback = async (feedbackData) => {
    const success = await submitFeedback(feedbackData);
    if (success) {
      setShowFeedbackModal(false);
      // Show success message
      alert(
        "Thank you for your feedback! This will help improve the bot's performance.",
      );
    }
  };

  const handleCloseFeedback = () => {
    setShowFeedbackModal(false);
    clearLastTestCallResult();
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50 font-inter">
      <ErrorNotification message={error} onDismiss={() => setError(null)} />

      <Header onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div
        className={`transition-all duration-300 p-4 lg:p-8 ${sidebarOpen ? "lg:ml-64" : "lg:ml-0"} pt-20 lg:pt-24`}
      >
        <div className="mb-6 lg:mb-8">
          <h2 className="text-2xl lg:text-3xl font-semibold text-[#101828] mb-2">
            Dashboard
          </h2>
          <p className="text-[#667085] text-sm lg:text-base">
            Monitor your outbound calling campaigns and appointments
          </p>
        </div>

        <SetupStatus
          setupStatus={setupStatus}
          checkEnvironmentSetup={checkEnvironmentSetup}
          isLoading={isActionLoading}
        />

        <StatsCards stats={stats} />

        <CampaignList
          campaigns={activeCampaigns}
          onToggle={toggleCampaign}
          onDelete={deleteCampaign}
          onShowNewCampaignModal={() => setShowNewCampaignModal(true)}
          onShowCallNumbersModal={() => setShowCallNumbersModal(true)}
          onShowTestCallModal={() => setShowTestCallModal(true)}
        />

        <AppointmentList
          appointments={recentAppointments}
          onCancel={cancelAppointment}
        />
      </div>

      <NewCampaignModal
        show={showNewCampaignModal}
        onClose={() => setShowNewCampaignModal(false)}
        onCreate={handleCreateCampaign}
        isLoading={isActionLoading}
      />

      <CallNumbersModal
        show={showCallNumbersModal}
        onClose={() => setShowCallNumbersModal(false)}
        onCall={handleCallNumbers}
        campaigns={activeCampaigns}
        isLoading={isActionLoading}
      />

      <TestCallModal
        show={showTestCallModal}
        onClose={() => setShowTestCallModal(false)}
        onTest={handleTestCall}
        campaigns={activeCampaigns}
        isLoading={isActionLoading}
      />

      <FeedbackModal
        show={showFeedbackModal}
        onClose={handleCloseFeedback}
        onSubmit={handleSubmitFeedback}
        campaignId={lastTestCallResult?.campaignId}
        campaignName={lastTestCallResult?.campaignName}
        isLoading={isActionLoading}
      />
    </div>
  );
}
