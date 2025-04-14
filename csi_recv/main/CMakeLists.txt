idf_component_register(SRC_DIRS "."
                       INCLUDE_DIRS "."
                       PRIV_REQUIRES mqtt
                       REQUIRES esp_wifi esp_netif nvs_flash esp_timer)
