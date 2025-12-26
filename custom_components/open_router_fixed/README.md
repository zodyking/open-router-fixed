# OpenRouter Fixed Integration for Home Assistant

A fixed and updated version of the OpenRouter integration for Home Assistant that works with the latest Home Assistant versions. This integration allows you to use OpenRouter's API to interact with various AI models as conversation agents in Home Assistant.

## Features

- ✅ **Conversation Agents**: Register and use OpenRouter AI models as conversation agents
- ✅ **Max Token Control**: Configure maximum tokens per request (1-32,000)
- ✅ **Advanced Parameters**: Control temperature, top_p, frequency_penalty, and presence_penalty
- ✅ **Model Selection**: Choose from any model available on OpenRouter
- ✅ **Options Flow**: Update settings after initial setup
- ✅ **Compatible with Latest Home Assistant**: Built for Home Assistant 2024.1+

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three dots menu (⋮) in the top right
4. Select **Custom repositories**
5. Add this repository URL: `https://github.com/zodyking/open-router-fixed`
6. Select **Integration** as the category
7. Click **Add**
8. Search for "OpenRouter Fixed" and install it
9. Restart Home Assistant
10. Go to **Settings** > **Devices & Services** > **Add Integration**
11. Search for "OpenRouter Fixed"

### Manual Installation

1. Copy the `custom_components/open_router_fixed` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services**
4. Click **Add Integration**
5. Search for "OpenRouter Fixed"

## Configuration

### Initial Setup

1. **Get an API Key**:
   - Go to [OpenRouter.ai](https://openrouter.ai/)
   - Sign up or log in
   - Navigate to **API Keys** in your account settings
   - Click **Create API Key**
   - Give it a name and set billing limits

2. **Add the Integration**:
   - Go to **Settings** > **Devices & Services** in Home Assistant
   - Click **Add Integration**
   - Search for "OpenRouter Fixed"
   - Enter your API key
   - Configure the following settings:
     - **Model**: The AI model to use (e.g., `openai/gpt-3.5-turbo`, `anthropic/claude-3-haiku`)
     - **Max Tokens**: Maximum tokens per response (1-32,000, default: 2048)
     - **Temperature**: Controls randomness (0.0-2.0, default: 0.7)
     - **Top P**: Nucleus sampling parameter (0.0-1.0, optional)
     - **Frequency Penalty**: Reduce repetition (-2.0 to 2.0, optional)
     - **Presence Penalty**: Encourage new topics (-2.0 to 2.0, optional)

### Updating Settings

After initial setup, you can update your settings:
1. Go to **Settings** > **Devices & Services**
2. Find your OpenRouter Fixed integration
3. Click on it, then click **Configure**
4. Update any settings you want to change

## Usage

Once configured, the OpenRouter integration will register as a conversation agent. You can:

- **Use in Voice Assistants**: The agent will be available in Home Assistant's voice assistant features
- **Use in Automations**: Call the conversation agent from automations
- **Use in Scripts**: Integrate AI responses into your scripts
- **Use in the UI**: Interact directly through Home Assistant's conversation interface

### Example Automation

```yaml
automation:
  - alias: "AI Response"
    trigger:
      - platform: conversation
        command: "turn on the lights"
    action:
      - service: conversation.process
        data:
          agent_id: "open_router_fixed"
          text: "{{ trigger.conversation.command }}"
```

## Supported Models

Any model available on OpenRouter can be used. Popular options include:

- `openai/gpt-3.5-turbo`
- `openai/gpt-4`
- `openai/gpt-4-turbo`
- `anthropic/claude-3-haiku`
- `anthropic/claude-3-sonnet`
- `anthropic/claude-3-opus`
- `google/gemini-pro`
- And many more...

Visit [OpenRouter.ai/models](https://openrouter.ai/models) to see all available models.

## Troubleshooting

### Integration Not Appearing

- Make sure the folder is named exactly `open_router_fixed`
- Ensure it's in the `custom_components` directory
- Restart Home Assistant completely

### API Errors

- Verify your API key is correct
- Check your OpenRouter account has sufficient credits
- Ensure billing limits are set correctly
- Check the Home Assistant logs for detailed error messages

### Conversation Not Working

- Verify the integration is loaded (check **Settings** > **Devices & Services**)
- Check that the conversation agent is enabled
- Review the logs for any errors

## Differences from Official Integration

This "Fixed" version includes:

- Updated code structure for latest Home Assistant versions
- Proper options flow for updating settings
- Better error handling
- Improved coordinator pattern implementation
- Support for all OpenRouter API parameters

## Support

For issues, feature requests, or questions:
- Check the Home Assistant logs
- Review the [OpenRouter API documentation](https://openrouter.ai/docs)
- Open an issue on the repository (if available)

## License

This integration is provided as-is for use with Home Assistant.

## Credits

- Built for Home Assistant community
- Uses OpenRouter API
- Based on the official OpenRouter integration structure

