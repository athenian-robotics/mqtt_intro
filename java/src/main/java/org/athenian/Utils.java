package org.athenian;

import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Utils {

    public static String getMqttHostname(String val) {
        return val.contains(":") ? val.substring(0, val.indexOf(":")) : val;
    }

    public static int getMqttPort(String s) {
        return s.contains(":") ? Integer.parseInt(s.substring(s.indexOf(":") + 1, s.length())) : 1883;
    }

    public static MqttClient createMqttClient(final String mqtt_hostname, final int mqtt_port, MqttCallback callback) {

        try {
            final MqttClient client = new MqttClient(String.format("tcp://%s:%d", mqtt_hostname, mqtt_port),
                                                     MqttClient.generateClientId(),
                                                     new MemoryPersistence());
            if (callback != null)
                client.setCallback(callback);
            System.out.println(String.format("Connecting to MQTT broker at %s:%d...", mqtt_hostname, mqtt_port));
            client.connect();
            System.out.println(String.format("Connected to %s:%d", mqtt_hostname, mqtt_port));
            return client;
        }
        catch (MqttException e) {
            e.printStackTrace();
            System.out.println(String.format("Cannot connect to MQTT broker at: %s:%d [%s]",
                                             mqtt_hostname, mqtt_port, e.getMessage()));
            return null;
        }
    }
}
