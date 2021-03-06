package org.athenian.args;

import com.beust.jcommander.JCommander;
import com.beust.jcommander.Parameter;
import com.beust.jcommander.ParameterException;
import org.eclipse.paho.client.mqttv3.MqttException;

public class BrokerArgs {
    @Parameter(names = {"-m", "--mqtt"}, required = true, description = "MQTT broker hostname")
    public String mqtt_arg;
    @Parameter(names = {"-h", "--help"}, help = true)
    private boolean help = false;

    public void parseArgs(final String programName, final String[] argv) throws MqttException {
        try {
            final JCommander jcom = new JCommander(this, argv);
            jcom.setProgramName(programName);

            if (this.help) {
                jcom.usage();
                System.exit(1);
            }

        }
        catch (ParameterException e) {
            System.out.println(e.getMessage());
            System.exit(1);
        }
    }
}
