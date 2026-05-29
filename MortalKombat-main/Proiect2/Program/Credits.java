package Proiect2.Program;

import Proiect2.Clase.Elemente;
import Proiect2.Clase.Menu;
import Proiect2.Clase.Sablon;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Credits extends Sablon implements ActionListener{
    public Credits(){

        Menu.eliminaActionListeners(5, 5, this);
        Image scaledImage = new ImageIcon("MortalKombat-main/Proiect2/Poze/EU.jpeg").getImage().getScaledInstance(500, 500, Image.SCALE_SMOOTH);
        ImageIcon poza=new ImageIcon(scaledImage);
        Elemente.labels[12].setPreferredSize(new Dimension(500, 500));
        Elemente.labels[12].setIcon(poza);
        Elemente.panels[0]= Menu.colorare(new ImageIcon("MortalKombat-main/Proiect2/Poze/ViVsye6.png").getImage());
        Elemente.panels[0].setLayout(new GridBagLayout());
        GridBagConstraints gbc=new GridBagConstraints();
        gbc.fill=GridBagConstraints.VERTICAL;
        gbc.anchor=GridBagConstraints.CENTER;
        gbc.weightx=0;
        gbc.gridx=0;
        gbc.gridy=0;
        gbc.insets=new Insets(0, 0, 400, 0);
        Elemente.panels[0].add(Elemente.labels[5], gbc);
        gbc.insets=new Insets(20, 0, 0, 0);
        Elemente.panels[0].add(Elemente.labels[12], gbc);
        gbc.gridy=1;
        Elemente.panels[0].add(Elemente.butoane[5], gbc);

        setContentPane(Elemente.panels[0]);

        setVisible(true);
    }
    public void actionPerformed(ActionEvent e){
        Menu.back(e, Elemente.butoane[5], this);
    }

}
