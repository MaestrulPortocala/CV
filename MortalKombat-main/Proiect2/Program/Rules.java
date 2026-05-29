package Proiect2.Program;

import Proiect2.Clase.Elemente;
import Proiect2.Clase.Menu;
import Proiect2.Clase.Sablon;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Rules extends Sablon implements ActionListener {

   public Rules() {

        Menu.eliminaActionListeners(11, 11, this);
        Image scroll = new ImageIcon("MortalKombat-main/Proiect2/Poze/scroll.png").getImage();
        Image scaledFoto = scroll.getScaledInstance(1100, 600, Image.SCALE_SMOOTH);
        Elemente.labels[13].setIcon(new ImageIcon(scaledFoto));
        Elemente.panels[0] = Menu.colorare(new ImageIcon("MortalKombat-main/Proiect2/Poze/rules.jpg").getImage());
        Elemente.panels[0].setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.VERTICAL;
        gbc.weightx = 0;
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.insets = new Insets(0, 0, 350, 0);
        Elemente.panels[0].add(Elemente.labels[4], gbc);
        gbc.insets = new Insets(0, 0, 0, 0);
        Elemente.panels[0].add(Elemente.labels[7], gbc);
        Elemente.panels[0].add(Elemente.labels[13], gbc);
        gbc.gridy = 1;
        Elemente.panels[0].add(Elemente.butoane[11], gbc);


        setContentPane(Elemente.panels[0]);
        setVisible(true);}
    public void actionPerformed(ActionEvent e) {
        Menu.back(e, Elemente.butoane[11], this);
    }
}
