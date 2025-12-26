# OpenRouter Fixed

A fixed and updated version of the OpenRouter integration for Home Assistant that works with the latest Home Assistant versions.

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
5. Add this repository URL
6. Select **Integration** as the category
7. Click **Add**
8. Search for "OpenRouter Fixed" and install it
9. Restart Home Assistant
10. Go to **Settings** > **Devices & Services** > **Add Integration**
11. Search for "OpenRouter Fixed"

### Manual Installation

1. Copy the `custom_components/open_router_fixed` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to **Settings** > **Devices & Services** > **Add Integration**
4. Search for "OpenRouter Fixed"

## Configuration

### Get an API Key

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up or log in
3. Navigate to **API Keys** in your account settings
4. Click **Create API Key**
5. Give it a name and set billing limits

### Setup

1. Go to **Settings** > **Devices & Services** in Home Assistant
2. Click **Add Integration**
3. Search for "OpenRouter Fixed"
4. Enter your API key
5. Configure the model and parameters:
   - **Model**: The AI model to use (e.g., `openai/gpt-3.5-turbo`)
   - **Max Tokens**: Maximum tokens per response (1-32,000, default: 2048)
   - **Temperature**: Controls randomness (0.0-2.0, default: 0.7)
   - **Top P**: Nucleus sampling parameter (0.0-1.0, optional)
   - **Frequency Penalty**: Reduce repetition (-2.0 to 2.0, optional)
   - **Presence Penalty**: Encourage new topics (-2.0 to 2.0, optional)

## Usage

Once configured, the OpenRouter integration will register as a conversation agent. You can use it in:
- Voice Assistants
- Automations
- Scripts
- Home Assistant's conversation interface

## Supported Models

Any model available on OpenRouter can be used. Popular options include:
- `openai/gpt-3.5-turbo`
- `openai/gpt-4`
- `anthropic/claude-3-haiku`
- `google/gemini-pro`
- And many more...

Visit [OpenRouter.ai/models](https://openrouter.ai/models) to see all available models.

## Differences from Official Integration

This "Fixed" version includes:
- Updated code structure for latest Home Assistant versions
- Proper options flow for updating settings
- Better error handling
- Improved coordinator pattern implementation
- Support for all OpenRouter API parameters

## Requirements

- Home Assistant 2024.1 or later
- OpenRouter API key
- Internet connection

## Links

- [OpenRouter Website](https://openrouter.ai/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)

