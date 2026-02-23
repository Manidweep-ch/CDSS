import "./ProfileAvatar.css";

function ProfileAvatar({ age, gender, size = "md" }) {
  const getAvatarStyle = () => {
    // Determine age group
    const ageGroup = age < 18 ? "child" : age < 60 ? "adult" : "senior";
    
    // Determine gender-based colors
    const genderColors = {
      Male: {
        primary: "#3B82F6",
        secondary: "#60A5FA",
        accent: "#93C5FD"
      },
      Female: {
        primary: "#EC4899",
        secondary: "#F472B6",
        accent: "#FBCFE8"
      },
      Other: {
        primary: "#8B5CF6",
        secondary: "#A78BFA",
        accent: "#C4B5FD"
      }
    };

    const colors = genderColors[gender] || genderColors.Other;

    return {
      background: `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`,
      ageGroup,
      colors
    };
  };

  const { background, ageGroup, colors } = getAvatarStyle();

  const sizeClasses = {
    sm: "avatar-sm",
    md: "avatar-md",
    lg: "avatar-lg",
    xl: "avatar-xl"
  };

  const getAvatarIcon = () => {
    if (ageGroup === "child") {
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="8" r="4"/>
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <path d="M12 12c-2 0-3 1-3 2"/>
        </svg>
      );
    } else if (ageGroup === "senior") {
      return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="8" r="4"/>
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <path d="M8 8h8"/>
          <path d="M9 12h6"/>
        </svg>
      );
    } else {
      // Adult
      if (gender === "Male") {
        return (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          </svg>
        );
      } else if (gender === "Female") {
        return (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <path d="M12 12v-1"/>
          </svg>
        );
      } else {
        return (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          </svg>
        );
      }
    }
  };

  return (
    <div 
      className={`profile-avatar ${sizeClasses[size]}`}
      style={{ background }}
    >
      <div className="avatar-icon">
        {getAvatarIcon()}
      </div>
      <div 
        className="avatar-glow" 
        style={{ background: colors.accent, opacity: 0.3 }}
      ></div>
    </div>
  );
}

export default ProfileAvatar;
