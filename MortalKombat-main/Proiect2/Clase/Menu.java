package Proiect2.Clase;

import Proiect2.Program.Home;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Menu {
    static public JButton[] configureButton(JButton[] button) {
        for (int i = 0; i < button.length; ++i) {
            button[i] = new JButton();
            if (i != 10) {
                button[i].setPreferredSize(new Dimension(200, 40));
                button[i].setMinimumSize(new Dimension(200, 40));
                button[i].setMaximumSize(new Dimension(200, 40));
            }
            button[i].setBackground(Color.RED);
            button[i].setForeground(Color.BLACK);
            button[i].setOpaque(true);
            button[i].setFocusable(false);
            button[i].setFont(new Font("MV Boli", Font.BOLD, 20));
            button[i].setBorder(BorderFactory.createEtchedBorder());
        }
        return button;
    }

    static public void configureLabels(JLabel[] label, int inceput, int sfarsit, int marime) {
        for (int i = inceput; i < sfarsit; ++i) {
            label[i] = new JLabel();
            label[i].setFont(new Font("MV Boli", Font.ITALIC, marime));
            label[i].setForeground(Color.RED);
        }
    }

    static public JPanel colorare(Image poza) {
        JPanel backgroundPanel = new JPanel(){
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.drawImage(poza, 0, 0, getWidth(), getHeight(), this);

            }
        };
        return backgroundPanel;
    }

    static public void back(ActionEvent e, JButton buton, Sablon object) {
        if (e.getSource() == buton) {
            new Home();
            object.dispose();
        }
    }

    static public void eliminaActionListeners(int inceput, int sfarsit, Sablon object) {
        for (int i = inceput; i <= sfarsit; ++i) {
            for (ActionListener al : Elemente.butoane[i].getActionListeners()) {
                Elemente.butoane[i].removeActionListener(al);
            }
            Elemente.butoane[i].addActionListener(object);
        }
    }

    static public JProgressBar configureHealthBar(String p, int health) {
        JProgressBar bar = new JProgressBar(0, 100);
        bar.setValue(health);
        bar.setStringPainted(true);
        bar.setString(p);
        bar.setFont(new Font("MV Boli", Font.ITALIC, 20));
        bar.setForeground(new Color(0, 200, 255));
        bar.setPreferredSize(new Dimension(450, 50));
        return bar;
    }

    static public JTextField configureTextFiled() {
       JTextField field = new JTextField();
        field.setPreferredSize(new Dimension(200, 40));
        field.setFont(new Font("MV Boli", Font.ITALIC, 25));
        field.setForeground(new Color(0, 200, 255));
        field.setBorder(BorderFactory.createEtchedBorder());
        field.setBackground(Color.BLACK);
        return field;
    }

    static public JPanel[] init_panel(JPanel[] panel) {
        for (int i = 1; i < panel.length; ++i) {
                panel[i] = new JPanel();
                panel[i].setOpaque(false);
                panel[i].setLayout(new FlowLayout(FlowLayout.CENTER, 20, 60));
        }
        return panel;
    }

    static public void reset(){
        Elemente.panels[1].removeAll();
        Elemente.labels[10].setVisible(false);
        Elemente.labels[11].setVisible(false);
        Elemente.butoane[10].setVisible(true);
        Elemente.labels[2].setText("FIGHT!!! ");
        Elemente.labels[2].setForeground(Color.RED);
    }


}







