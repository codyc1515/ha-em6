# em6 Energy Price integration for Home Assistant
## Getting started
In your configuration.yaml file, add the following:

```
sensor:
  - platform: em6
    location: Christchurch # Grid Zone Name
```
The list of Grid Zone Names (Locations) is available at https://app.em6.co.nz/

## Installation
### HACS (recommended)
1. [Install HACS](https://hacs.xyz/docs/setup/download), if you did not already
2. [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=codyc1515&repository=ha-em6&category=integration)
3. Install the em6 Energy Price integration
4. Restart Home Assistant

### Manually
Copy all files in the custom_components/em6 folder to your Home Assistant folder *config/custom_components/em6*.

## Known issues
None known.

## Future enhancements
Your support is welcomed.
