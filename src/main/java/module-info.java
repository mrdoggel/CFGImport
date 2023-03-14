module cfgimport.cfgimport {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;

    opens cfgimport.cfgimport to javafx.fxml;
    exports cfgimport.cfgimport;
}