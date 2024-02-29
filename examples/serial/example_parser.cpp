#include <sstream>
#include <string>
#include <vector>


// A pretty standard splitString implementation.
std::vector<std::string> splitString(std::string str, char delimiter)
{
    std::vector<std::string> splitVect;
    std::stringstream ss(str);
    std::string substr;

    while (ss.good())
    {
        getline(ss, substr, delimiter);
        splitVect.emplace_back(std::move(substr));
    }
    return splitVect;
}

/**
 * @brief Takes a string formatted to be a response and returns the original message, the
 * timestamp, any errors and/or the values returned by the backend, if any.
 * Example: "%?STTN=1 2_\r" would return std::vector<std::string> {"?STTN", "1 0"} with 1
 * being the nanoseconds since the epoch and 0 being the station status }
 *
 * @param[in]  response_string  The formatted string response, returned by the API
 *
 * @return A std::vector<std::string> of the original message and the response to the message
 * with delimiters stripped out.
 */
std::vector<std::string> ParseResponse(std::string response_string)
{
    // The response string is split around a single equals sign '='. There will never be more than one (1) equals
    // sign in a response string.
    std::vector<std::string> split_response = splitString(response_string.substr(1), '=');

    // Strip the leading percent '%' which is indicative of a response. Logic can be performed here to verify that
    // the message is a properly formatted response.
    std::string s = split_response[1];

    // The underscore '_' indicate the end of a response. It will be in the second slot of the vector along with the
    // timestamp and returned values. Strip any characters after it.
    int loc = s.find('_');
    split_response[1] = s.substr(0, loc);

    // Determine if there were any errors
    if (split_response[1].find("#ERR") != split_response[1].npos)
    {
        std::string command = split_response[0];
        // If there were errors, update the 0th item in the split response to reflect that.
        split_response[0] = "API Returned an error for command " + command + ".";
    }

    // Return the vector so it is known what response matches what original command.
    return split_response;
}
