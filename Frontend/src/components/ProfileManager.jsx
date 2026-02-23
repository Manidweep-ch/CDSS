import { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";
import "./ProfileManager.css";

function ProfileManager({ onProfileSelect, activeProfile }) {
  const [profiles, setProfiles] = useState([]);
  const [profileName, setProfileName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [showForm, setShowForm] = useState(false);

  const fetchProfiles = async () => {
    try {
      const response = await axiosClient.get("/profiles/");
      setProfiles(response.data);
    } catch (err) {
      console.error("Failed to fetch profiles:", err);
      alert("Failed to load profiles. Please try again.");
    }
  };

  useEffect(() => {
    fetchProfiles();
  }, []);

  const createProfile = async () => {
    if (!profileName.trim()) {
      alert("Profile name is required");
      return;
    }

    if (age && (isNaN(age) || parseInt(age) < 0 || parseInt(age) > 150)) {
      alert("Please enter a valid age (0-150)");
      return;
    }

    try {
      await axiosClient.post("/profiles/", {
        profile_name: profileName,
        age: age ? parseInt(age) : null,
        gender,
      });

      setProfileName("");
      setAge("");
      setGender("");
      setShowForm(false);
      await fetchProfiles();
    } catch (err) {
      console.error("Failed to create profile:", err);
      alert(`Failed to create profile: ${err.response?.data?.detail || err.message}`);
    }
  };

  const deleteProfile = async (profileId, profileName) => {
    if (!confirm(`Are you sure you want to delete profile "${profileName}"? This will also delete all associated evaluations.`)) {
      return;
    }

    try {
      await axiosClient.delete(`/profiles/${profileId}`);
      
      if (activeProfile === profileId) {
        onProfileSelect(null);
      }
      
      await fetchProfiles();
      alert("Profile deleted successfully");
    } catch (err) {
      console.error("Failed to delete profile:", err);
      alert(`Failed to delete profile: ${err.response?.data?.detail || err.message}`);
    }
  };

  return (
    <div className="profile-manager fade-in">
      <div className="profile-header">
        <div>
          <h2>Patient Profiles</h2>
          <p>Manage patient information and medical records</p>
        </div>
        <button 
          className="btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          {showForm ? "Cancel" : "New Profile"}
        </button>
      </div>

      {showForm && (
        <div className="profile-form slide-in">
          <div className="form-row">
            <div className="form-group">
              <label>Profile Name *</label>
              <input
                type="text"
                value={profileName}
                onChange={(e) => setProfileName(e.target.value)}
                placeholder="Enter patient name"
              />
            </div>
            <div className="form-group">
              <label>Age</label>
              <input
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age"
                min="0"
                max="150"
              />
            </div>
            <div className="form-group">
              <label>Gender</label>
              <select
                value={gender}
                onChange={(e) => setGender(e.target.value)}
              >
                <option value="">Select</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          <button className="btn-primary" onClick={createProfile}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            Create Profile
          </button>
        </div>
      )}

      <div className="profiles-grid">
        {profiles.length === 0 && (
          <div className="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            <h3>No profiles yet</h3>
            <p>Create a patient profile to get started</p>
          </div>
        )}

        {profiles.map((profile) => (
          <div 
            key={profile.id}
            className={`profile-card ${activeProfile === profile.id ? 'active' : ''}`}
          >
            <div className="profile-avatar">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            </div>
            <div className="profile-info">
              <h3>{profile.profile_name}</h3>
              <div className="profile-meta">
                {profile.age && <span>Age: {profile.age}</span>}
                {profile.gender && <span>• {profile.gender}</span>}
              </div>
            </div>
            <div className="profile-actions">
              <button 
                className={`btn-select ${activeProfile === profile.id ? 'active' : ''}`}
                onClick={() => onProfileSelect(profile.id)}
              >
                {activeProfile === profile.id ? (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="20 6 9 17 4 12"/>
                    </svg>
                    Active
                  </>
                ) : (
                  "Select"
                )}
              </button>
              <button 
                className="btn-delete"
                onClick={() => deleteProfile(profile.id, profile.profile_name)}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProfileManager;
