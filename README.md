# Home Assistant Integration: Napoleon Grill

**Napoleon Grill** is a custom integration for [Home Assistant](https://www.home-assistant.io/) that allows you to monitor your Napoleon smart grill (via the [Ayla Networks](https://www.aylanetworks.com/) IoT platform) directly in Home Assistant – e.g. for dashboards, automations, or notifications.

> ⚠️ Note: This integration is currently in development. Feedback and pull requests are welcome!

> ⚠️ Currently only the EU region is supported.

---

## 🔥 Features

- Monitor up to 4 temperature probes in real-time
- Grill connection status
- WiFi signal strength (RSSI)
- Brightness & burner level
- Probe status monitoring
- Automations based on grill state (e.g. notify when target temperature is reached)

---

## 🛠️ Installation (via HACS)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant.
2. Open HACS → **Integrations** → Menu (top right) → **Custom repositories**.
3. Enter the following GitHub repository: [https://github.com/KoblerS/napoleon-hacs](https://github.com/KoblerS/napoleon-hacs) and select type: **Integration**
4. Search for "Napoleon Grill" and install the integration.
5. Restart Home Assistant.

---

## ⚙️ Configuration

After installation, you can add the integration via the UI:

1. Go to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for "Napoleon Grill" and follow the setup steps.
3. Enter your Napoleon Home app credentials (email & password) and select your region.

---

## 📡 Supported Devices

- Napoleon Prestige 500 (Prestige-CCF)

---

## 🌍 Supported Regions

- EU (more regions planned)

---

## ℹ️ Disclaimer

This Home Assistant integration was developed independently and is not affiliated with Napoleon or Ayla Networks.
All trademarks, names, logos, and content of the Napoleon Home app are the property of their respective owners.
This integration is provided purely for technical extension in an open-source context and without commercial intent.
For support or questions about the Napoleon Home app, please contact the official provider.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are very welcome!
Feel free to create an issue or submit a pull request.
