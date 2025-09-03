
<p align="center">
  <a href="https://github.com/tu-utente/guardia-vento-tende/actions/workflows/validate.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/tu-utente/guardia-vento-tende/validate.yml?label=validate&logo=github" alt="Validate">
  </a>
  <a href="https://github.com/hacs/integration">
    <img src="https://img.shields.io/badge/HACS-Custom-orange.svg?logo=homeassistant" alt="HACS">
  </a>
  <a href="https://img.shields.io/github/v/release/tu-utente/guardia-vento-tende">
    <img src="https://img.shields.io/github/v/release/tu-utente/guardia-vento-tende?logo=github" alt="Release">
  </a>
</p>


# Guardia Vento Tende (Home Assistant)

Integrazione custom in italiano per proteggere le tende da sole in base alla velocità del vento (fonte: Open-Meteo, nessuna API key).
Include:
- **Config Flow UI** (impostazioni e opzioni dall'interfaccia)
- **Isteresi a cicli** (attivazione/disattivazione dopo N cicli sopra/sotto soglia)
- **Logging dettagliato** (livello DEBUG/INFO)
- **Servizio manuale** `guardia_vento_tende.aggiorna_dati`

## Installazione
1. Copia `custom_components/guardia_vento_tende/` in `config/custom_components/`.
2. Riavvia Home Assistant.
3. Aggiungi l'integrazione da Impostazioni → Dispositivi & Servizi → "Aggiungi integrazione" → **Guardia Vento Tende**.
4. (Opzionale) Importa la blueprint da `blueprints/automation/guardia_vento_tende/guardia_vento.yaml`.

## Opzioni
- `Soglia (km/h)` (default 35)
- `Intervallo aggiornamento (s)` (default 300)
- `Usa coordinate Home Assistant` oppure lat/lon personalizzate
- `Cicli sopra soglia per attivare` (default 2)
- `Cicli sotto soglia per disattivare` (default 2)

## Entità
- `sensor.velocita_vento` / `sensor.raffiche_vento`
- `binary_sensor.allerta_vento_tende`

## Servizi
- `guardia_vento_tende.aggiorna_dati` → forza l'aggiornamento dei dati.



## Installazione con HACS (consigliata)

1. In HACS → Integrazioni → Menu ⋮ → **Custom repositories** → incolla l'URL del tuo repo e scegli categoria **Integration**.
2. Apri l'integrazione **Guardia Vento Tende** e premi **Installa**.
3. Riavvia Home Assistant.
4. Vai su **Impostazioni → Dispositivi e servizi → Aggiungi integrazione** e cerca **Guardia Vento Tende**.


## Rilasci

- Crea un tag in GitHub (es. `v1.1.0`) → il workflow **Release** pubblica automaticamente lo ZIP pronto per HACS.
