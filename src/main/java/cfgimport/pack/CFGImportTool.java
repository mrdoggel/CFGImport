package cfgimport.pack;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

import java.io.*;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

public class CFGImportTool extends Application {
    @Override
    public void start(Stage stage) {
        Pane pane = new Pane();
        decorate(pane);
        try {
            downloadImages();
        } catch (IOException e) {
            System.out.print(e);
        }
        /*
        Scene scene = new Scene(pane);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();*/
    }

    public void decorate(Pane pane) {

    }

    public void downloadImages() throws IOException {
        URL url = new URL("http://cfgimport.com/uploads/60299724/config.cfg");
        ReadableByteChannel rbc = Channels.newChannel(url.openStream());
        FileOutputStream fos = new FileOutputStream("config.cfg");
        fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
        fos.close();
        rbc.close();
        //FileUtils.copyURLToFile(URL, File)
    }

    public static void main(String[] args) {
        launch();
    }
}