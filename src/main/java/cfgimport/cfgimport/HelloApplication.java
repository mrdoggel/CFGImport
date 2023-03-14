package cfgimport.cfgimport;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

import java.io.IOException;

public class HelloApplication extends Application {
    @Override
    public void start(Stage stage) {
        Pane pane = new Pane();
        decorate(pane);
        Scene scene = new Scene(pane);
        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.show();
    }

    public void decorate(Pane pane) {

    }

    public static void main(String[] args) {
        launch();
    }
}