package Proiect2.Program;

import Proiect2.Clase.Elemente;
import Proiect2.Clase.Menu;
import Proiect2.Clase.Sablon;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class FATALITY extends Sablon implements ActionListener{
    FATALITY(String nume, Image poza){

        Menu.eliminaActionListeners(11, 11, this);
        Elemente.labels[6].setText(nume+" WINS ");
        Elemente.labels[14].setIcon(new ImageIcon(poza));
        Elemente.panels[0]=new JPanel();
        Elemente.panels[0].setBackground(Color.BLACK);
        Elemente.panels[0].setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill=GridBagConstraints.VERTICAL;
        gbc.gridx=0;
        gbc.gridy=0;
        Elemente.panels[0].add(Elemente.labels[6], gbc);
        gbc.gridy=1;
        Elemente.panels[0].add(Elemente.labels[3], gbc);
        gbc.gridy=2;
        Elemente.panels[0].add(Elemente.labels[14], gbc);
        gbc.gridy=3;
        gbc.insets=new Insets(0, 0, 50, 0);
        Elemente.panels[0].add(Elemente.butoane[11], gbc);
        setContentPane(Elemente.panels[0]);
        setVisible(true);
    }
    public void actionPerformed(ActionEvent e){
        Menu.back(e, Elemente.butoane[11], this);
    }

}
