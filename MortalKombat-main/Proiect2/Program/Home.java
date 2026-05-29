package Proiect2.Program;
import Proiect2.Clase.Elemente;
import Proiect2.Clase.Menu;
import Proiect2.Clase.Sablon;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import static Proiect2.Clase.Elemente.musicPlayer;

public class Home extends Sablon implements ActionListener {

    public Home() {
        Menu.eliminaActionListeners(0, 3, this);
        Elemente.panels[0]= Menu.colorare(new ImageIcon("MortalKombat-main/Proiect2/Poze/main.png").getImage());
        Elemente.panels[0].setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill=GridBagConstraints.VERTICAL;
        gbc.weightx=0;
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.NORTH;
        gbc.insets = new Insets(0, 0, 0, 0);
        Elemente.panels[0].add(Elemente.labels[0], gbc);
        gbc.gridy=1;
        gbc.insets = new Insets(0, 0, 100, 0);
        Elemente.panels[0].add(Elemente.labels[1], gbc);
        gbc.gridy=2;
        gbc.insets = new Insets(0, 0, 20, 0);
        Elemente.panels[0].add(Elemente.butoane[0], gbc);
        gbc.gridy=3;
        Elemente.panels[0].add(Elemente.butoane[1], gbc);
        gbc.gridy=4;
        Elemente.panels[0].add(Elemente.butoane[2], gbc);
        gbc.gridy=5;
        gbc.insets = new Insets(0, 0, 200, 0);
        Elemente.panels[0].add(Elemente.butoane[3], gbc);
        setContentPane(Elemente.panels[0]);

        setVisible(true);
    }


    public void actionPerformed(ActionEvent e) {
       if (e.getSource() == Elemente.butoane[0]) {
            new Names();
            dispose();
        }
        else if(e.getSource()== Elemente.butoane[1]){
            new Rules();
            dispose();
        }
        if (e.getSource() == Elemente.butoane[2]) {
            new Credits();
            dispose();
        }
        else if(e.getSource()== Elemente.butoane[3]){
            Elemente.play=false;
            musicPlayer.stopMusic();
            dispose();
        }
    }


}
