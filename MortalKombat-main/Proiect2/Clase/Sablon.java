package Proiect2.Clase;
import java.awt.*;
import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Sablon extends JFrame implements ActionListener {
    public Sablon() {
        ImageIcon image = new ImageIcon("MortalKombat-main/Proiect2/Poze/download.jpg");
        setIconImage(image.getImage());
        setTitle("MORTAL KOMBAT DUMBRAVIOARA EDITION");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        setSize(screenSize);
        setLocation(0, 0);
        setUndecorated(true);

    }

    public void actionPerformed(ActionEvent e) {

    }
}
