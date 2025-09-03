# Guardia Vento Tende (Home Assistant)

Integrazione custom in italiano per proteggere le tende da sole in base alla velocità del vento (Open-Meteo, nessuna API key).
- **Config Flow UI** (impostazioni dall'interfaccia)
- **Isteresi a cicli**
- **Logging dettagliato**
- **Servizio** `guardia_vento_tende.aggiorna_dati`

## Installazione HACS
1. HACS → Integrazioni → ⋮ → Custom repositories → URL repo → categoria *Integration*.
2. Installa e riavvia HA.
3. Impostazioni → Dispositivi e servizi → Aggiungi integrazione → *Guardia Vento Tende*.

## Log di debug
```yaml
logger:
  logs:
    custom_components.guardia_vento_tende: debug
```

