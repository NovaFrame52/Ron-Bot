```markdown
# Privacy Policy for Ron Discord Bot

**Last Updated: February 10, 2026**

## 1. Introduction

This Privacy Policy explains how the Ron Discord bot ("Ron", "the Bot", "we", "us") collects, uses, and protects information when you use our service. We are committed to transparency about our data practices.

## 2. Information We Collect

### 2.1 Automatically Collected Information

When Ron operates in your Discord server, the Bot automatically collects:

- **User Information**: Discord user ID and username of users who interact with the Bot
- **Server Information**: Server/guild ID where the Bot is present
- **Channel Information**: Channel IDs where commands are used
- **Command Usage**: Content of messages that invoke Bot commands (both prefix and slash commands)
- **Reminder Data**: User-provided reminder messages and times (temporary, in-memory only)
- **Timestamps**: When interactions occur

### 2.2 Subscription Data

For users who subscribe to water reminders:

- **User IDs**: Stored in-memory in a set (`WATER_REMINDER_USERS`) to track subscribers
- **Subscription Status**: Whether a user is subscribed or unsubscribed
- This data is stored only in memory and is lost when the Bot restarts

### 2.3 Log Data

Ron maintains logs for debugging and operational purposes, stored locally in `ron.log`. These logs may include:

- Command invocations
- Error messages and stack traces
- User IDs involved in errors
- Timestamps of events
- Bot startup and connection events

### 2.4 Configuration Data

Server configuration data stored in `configs.json` may include:

- Server/guild IDs
- Bot configuration settings (if any are added in future versions)

### 2.5 Information We Do NOT Collect

Ron does not collect, store, or process:

- Message content from messages that don't invoke the Bot
- Private conversations between users
- User email addresses or personal contact information beyond Discord usernames
- Voice chat data
- Attachments or media files (except temporarily to relay DM images via the DM command)
- Personal health data, medical information, or fitness tracking data
- Payment or financial information
- Messages in channels where the Bot lacks access

## 3. How We Use Information

We use collected information solely for the following purposes:

- **Bot Operation**: To execute commands and provide Bot functionality
- **Reminder Delivery**: To send reminders at requested times via DM
- **Water Reminders**: To send hourly hydration reminders to subscribed users
- **Command Processing**: To parse and respond to user commands
- **Logging & Debugging**: To diagnose issues, monitor performance, and improve the Bot
- **DM Functionality**: To send direct messages on behalf of the authorized user

## 4. Data Storage and Retention

### 4.1 Storage Location

All data is stored locally on the server where Ron is deployed:

- **In-Memory Data**: Water reminder subscriptions and active reminder tasks are stored only in RAM
- **Log Files**: Stored in `ron.log` in the project root directory
- **Configuration**: Minimal config data stored in `configs.json` in the project root
- **No Cloud Storage**: No data is transmitted to external servers or cloud services except Discord's API for Bot operations

### 4.2 Retention Period

- **Water Reminder Subscriptions**: Stored in memory only; lost when Bot restarts
- **Active Reminders**: Stored in memory only; lost when Bot restarts
- **Log Files**: Retained indefinitely unless manually deleted by the server administrator
- **Configuration Data**: Retained indefinitely in `configs.json` unless manually deleted

### 4.3 Data Deletion

- Server administrators can delete log files and configuration files at any time from their local filesystem
- Removing Ron from a server immediately stops all data collection from that server
- Users can unsubscribe from water reminders at any time using the `!waterreminder` or `/waterreminder` command
- Self-hosters have full control over all data stored by their deployment

## 5. Data Sharing and Disclosure

### 5.1 Third-Party Sharing

We do NOT sell, trade, rent, or share your data with third parties for marketing or any other purposes.

### 5.2 Discord Platform

Ron uses Discord's API to function and necessarily shares data with Discord according to Discord's own Privacy Policy and Terms of Service. This includes:

- Message content the Bot reads (for command processing)
- Responses the Bot sends to channels and users
- Slash command interactions
- Direct messages sent via the Bot

### 5.3 Legal Requirements

We may disclose information if required by law, such as to comply with a subpoena or similar legal process. However, as Ron is primarily self-hosted, server administrators control their own data.

## 6. Data Security

We take reasonable measures to protect collected data:

- Log files and configuration files are stored with standard file system permissions
- Access to the server is controlled by the server administrator
- The Bot runs under standard user privileges
- Environment variables (including the Discord token) are stored in `.env` files with restricted permissions (600)
- The installer automatically sets restrictive permissions on configuration files
- Water reminder subscription data is stored only in memory (not on disk)

However, no method of electronic storage is 100% secure. While we strive to protect your information, we cannot guarantee absolute security. Self-hosters are responsible for securing their own deployments.

## 7. Your Rights and Choices

### 7.1 Self-Hosted Deployments

Server administrators who self-host Ron can:

- View, modify, or delete all log files and configuration files at any time
- Control where data is stored
- Access the complete source code to verify data handling practices
- Modify the Bot's code to change data collection practices

### 7.2 End Users

Discord users can:

- Subscribe and unsubscribe from water reminders at any time
- Avoid using the Bot's features to minimize data collection
- Request that server administrators remove the Bot
- Leave servers where Ron is present
- Disable DMs to prevent receiving reminders

### 7.3 Data Access and Deletion Requests

To request information about data collected about you, or to request deletion:

- Contact the administrator of the server where Ron is deployed
- For self-hosted instances, server administrators can directly access and delete data files
- Unsubscribe from water reminders using the `!waterreminder` or `/waterreminder` command

## 8. Children's Privacy

Ron does not knowingly collect information from children under 13 (or the applicable age in your jurisdiction). The Bot relies on Discord's age verification. If you believe we have inadvertently collected information from a child, please contact the server administrator.

## 9. Open Source Transparency

Ron is open source software released under the MIT License. You can review the complete source code to verify:

- What data is collected
- How data is processed and stored
- Where data is stored
- How data is used
- Security practices implemented

## 10. Discord's Policies

Ron operates on Discord's platform and is subject to:

- Discord's Privacy Policy
- Discord's Terms of Service
- Discord's Developer Terms of Service
- Discord's Community Guidelines

We recommend reviewing Discord's privacy documentation at https://discord.com/privacy

## 11. Self-Hosting Considerations

If you self-host Ron, you should be aware:

- You are the data controller for your deployment
- You are responsible for securing your environment and configuration files
- You must protect your Discord bot token (stored in `.env`)
- You are responsible for managing and securing log files
- You should configure appropriate file permissions and access controls
- You should regularly review and clean up log files to prevent excessive data accumulation

## 12. International Users

Ron may be deployed on servers located in various jurisdictions. Data is stored locally on the server where the Bot runs. By using the Bot, you consent to the transfer and processing of your information in the jurisdiction where that specific Bot deployment is located.

## 13. Changes to This Privacy Policy

We may update this Privacy Policy from time to time. Changes will be indicated by updating the "Last Updated" date at the top of this policy. Material changes will be communicated through:

- Updates to the project repository
- Documentation in the README file
- Notifications to server administrators (where feasible)

```