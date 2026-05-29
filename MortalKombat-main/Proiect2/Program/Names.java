package Proiect2.Program;

import Proiect2.Clase.*;
import Proiect2.Clase.Menu;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Names extends Sablon implements ActionListener {
    static public Player p1=new Player();
    static public Player p2=new Player();
    JTextField name1, name2;
    Names() {

        Menu.eliminaActionListeners(4, 4, this);
        name1 = Menu.configureTextFiled();
        name2 = Menu.configureTextFiled();
        name2.setForeground(Color.RED);
        Elemente.panels[0]= Menu.colorare(new ImageIcon("MortalKombat-main/Proiect2/Poze/name.jpg").getImage());
        Elemente.labels[8].setForeground(new Color(0,200,255));
        Elemente.panels[0].setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.VERTICAL;
        gbc.weightx = 0;
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.insets = new Insets(0, 0, 0, 0);
        Elemente.panels[0].add(Elemente.labels[8], gbc);
        gbc.gridy=1;
        Elemente.panels[0].add(name1, gbc);
        gbc.gridy=2;
        gbc.insets = new Insets(40, 0, 0, 0);
        Elemente.panels[0].add(Elemente.labels[9], gbc);
        gbc.gridy=3;
        gbc.insets = new Insets(0, 0, 0, 0);
        Elemente.panels[0].add(name2, gbc);
        gbc.gridy=4;
        gbc.insets = new Insets(40, 0, 0, 0);
        Elemente.panels[0].add(Elemente.butoane[4], gbc);

        setContentPane(Elemente.panels[0]);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {

        Menu.back(e, Elemente.butoane[11], this);
        if (e.getSource() == Elemente.butoane[4]) {
            if(name1.getText().equals(name2.getText())){
                JOptionPane.showMessageDialog(this, "Both players can't have the same name...", "Same name error...", JOptionPane.ERROR_MESSAGE);
            }
            else {
                p1.setName(name1.getText());
                p2.setName(name2.getText());
                new Kombat();
                dispose();
            }
        }
    }



}