import subprocess
import re

try:
    # Running the (netsh wlans show profile command) and capture the output into a variable
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

    # Using regular expressions to grep the string we want from the above command output and save it into a variable
    profile_names = set(re.findall(r"All User Profile\s+:\s+(.*)", command_output))

    # This will store the Wi-Fi SSIDs and their corresponding passwords (SSID: password)
    wifi_data = ""

    # Iterate through the profile names
    for profile in profile_names:
        # Remove trailing whitespaces and newline characters
        profile = profile.strip()

        # Show the profile details together with the clear text password
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"],
                                      capture_output=True).stdout.decode()

        # Use regular expressions to search for the password
        profile_password = re.findall(r"Key Content\s+:\s+(.*)", profile_info)

        # Check to see if the profile has a password
        if len(profile_password) == 0:
            wifi_data += f"{profile}: Open\n"
        else:
            wifi_data += f"{profile}: {profile_password[0].strip()}\n"

    # Save the Wi-Fi details in a file
    with open("wifis.txt", "w") as file:
        file.write(wifi_data)

    print("Wi-Fi data has been saved to 'wifis.txt' successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
