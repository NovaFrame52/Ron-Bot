# Privacy Policy for Ron Discord Bot

**Last Updated: February 7, 2026**

## 1. Introduction

This Privacy Policy explains how the Ron Discord bot ("Ron", "the Bot", "we", "us") collects, uses, and protects information when you use our service. We are committed to transparency about our data practices.

## 2. Information We Collect

### 2.1 Automatically Collected Information

When Ron operates in your Discord server, the Bot automatically collects:

- **User Information**: Discord user ID and username of users who interact with the Bot
- **Server Information**: Server/guild ID where the Bot is present
- **Channel Information**: Channel IDs where commands are used
- **Command Usage**: Content of messages that invoke Bot commands (both prefix and slash commands)
- **Weather Queries**: City names requested for weather information
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
- Weather API request outcomes
- Bot startup and connection events

### 2.4 Configuration Data

Server configuration data stored in `configs.json` may include:

- Server/guild IDs
- Bot configuration settings (if any are added in future versions)

Note: As of the current version, Ron stores minimal persistent configuration data.

### 2.5 Information We Do NOT Collect

Ron does not collect, store, or process:

- Message content from messages that don't invoke the Bot
- Private conversations between users
- User email addresses or personal contact information beyond Discord usernames
- Voice chat data
- Attachments or media files (except temporarily to relay DM images via the DM command)
- Personal health data, medical information, or fitness tracking data
- Location data beyond city names provided for weather queries
- Payment or financial information
- Messages in channels where the Bot lacks access

## 3. How We Use Information

We use collected information solely for the following purposes:

- **Bot Operation**: To execute commands and provide Bot functionality
- **Weather Service**: To fetch and display weather information for requested cities
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
- **No Cloud Storage**: No data is transmitted to external servers or cloud services (except Discord's API for Bot operations and wttr.in for weather data)

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

### 5.3 Weather API (wttr.in)

When users request weather information, the Bot sends HTTP requests to the wttr.in API containing:

- City names provided by users
- No personal identifiers are sent to the weather API
- wttr.in may log requests according to their own privacy policies

### 5.4 Legal Requirements

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

The source code is available in the project repository and can be audited by anyone.

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

Continued use of Ron after changes constitutes acceptance of the updated Privacy Policy.

## 14. Data Breach Notification

In the event of a data breach affecting user information:

- Self-hosters are responsible for their own breach response
- For any managed instances, we will assess the scope and impact
- We will take immediate steps to secure systems
- We will notify affected parties as required by applicable law

However, given Ron's self-hosted nature and minimal data collection, individual deployments are the responsibility of their operators.

## 15. Specific Data Practices

### 15.1 Water Reminder System

- User IDs are stored in an in-memory set (`WATER_REMINDER_USERS`)
- This data is NOT persisted to disk
- Subscription status is lost when the Bot restarts
- Reminder messages are sent via Discord DM
- No hydration tracking data is collected or stored
- Unsubscribing immediately removes the user ID from the in-memory set

### 15.2 Weather Queries

- City names are sent to wttr.in API in real-time
- No weather query history is stored locally
- Weather data is fetched on-demand and not cached
- The Bot does not log which users requested which cities (except in error logs)
- wttr.in may log requests according to their own policies

### 15.3 Personal Reminders

- Reminder messages and times are stored only in memory (asyncio tasks)
- Reminders are not persisted to disk
- All active reminders are lost if the Bot restarts
- Reminder content is temporarily processed but not logged
- Reminders are delivered via Discord DM

### 15.4 Wellness Features

- No usage tracking for wellness commands (workout, breathing, tip, motivate)
- No personal health or fitness data is collected
- Command usage may appear in general logs (command name only)
- Content is selected randomly from predefined lists

### 15.5 DM Functionality

- The DM command allows a restricted user to send messages to server members
- Message content is temporarily processed but not stored (beyond general logs)
- Image attachments are relayed through Discord's infrastructure
- Access is restricted via the `ALLOWED_DM_USER_ID` configuration
- The Bot does not log DM content (except in error scenarios)

### 15.6 Logging Practices

The `ron.log` file may contain:

- Timestamps of events
- Command invocations (command names, not full content)
- Error messages with stack traces
- User IDs involved in errors
- Connection status and Bot lifecycle events
- Weather API request results
- Minimal command execution details

Logs do NOT contain:

- Full message content
- Personal health information
- Passwords or tokens
- Detailed user conversations

## 16. GDPR Compliance (European Users)

For users in the European Economic Area, you have the following rights under GDPR:

- **Right to Access**: Request copies of your data from server administrators
- **Right to Rectification**: Request correction of inaccurate data
- **Right to Erasure**: Request deletion of your data (contact server administrator)
- **Right to Restrict Processing**: Request limited processing of your data
- **Right to Data Portability**: Request transfer of your data
- **Right to Object**: Object to processing of your data

To exercise these rights, contact the administrator of the server where Ron is deployed. For self-hosted instances, administrators can directly access and modify data files.

## 17. California Privacy Rights (CCPA)

California residents have the right to:

- Know what personal information is collected
- Know whether personal information is sold or disclosed (we do not sell data)
- Opt-out of the sale of personal information (not applicable as we don't sell data)
- Request deletion of personal information
- Non-discrimination for exercising privacy rights

Contact your server administrator to exercise these rights.

## 18. Limitations

This Privacy Policy applies only to Ron and does not cover:

- Other bots on the same Discord server
- Discord's own data practices
- Third-party services (wttr.in weather API)
- Other software or services you may use
- Data practices of individual self-hosted deployments (beyond what the code implements)

## 19. No Health Data Collection

**IMPORTANT**: Ron does NOT collect, store, or process:

- Personal health information (PHI)
- Medical records or history
- Fitness tracking data
- Hydration tracking data (beyond subscription status)
- Body measurements or vital signs
- Dietary information
- Sleep data
- Any protected health information under HIPAA or similar regulations

Wellness features provide general suggestions only and do not involve health data collection.

## 20. Contact Information

For questions, concerns, or requests regarding this Privacy Policy or your data:

- Contact the administrator of the server where Ron is deployed
- For self-hosted instances, you control all data directly
- File an issue in the project's code repository for questions about data practices
- Review the source code to verify data handling

## 21. Responsibility for Self-Hosted Instances

While this Privacy Policy describes the data practices implemented in Ron's source code, individual server administrators who self-host the Bot are responsible for:

- Their own privacy policies and notices to users
- Compliance with applicable privacy laws in their jurisdiction
- Securing their deployment and protecting stored data
- Managing data retention and deletion
- Responding to data access and deletion requests from their users
- Ensuring .env files and tokens are properly secured

---

**By using Ron, you acknowledge that you have read and understood this Privacy Policy.**