module cfgimport.cfgimport {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;

    opens cfgimport.pack to javafx.fxml;
    exports cfgimport.pack;
}