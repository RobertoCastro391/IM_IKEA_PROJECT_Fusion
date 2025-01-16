/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.IOException;
import scxmlgen.Fusion.FusionGenerator;
//import FusionGenerator;
import Modalities.Gestures;
import Modalities.Output;
import Modalities.Speech;

/**
 *
 * @author nunof
 */
public class GenFusionSCXML {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {

        FusionGenerator fg = new FusionGenerator();

        // Complementary
        fg.Complementary(Speech.REMOVE_PRODUCT_CART, Gestures.REMOVE, Output.REMOVE_PRODUCT_CART);
        fg.Complementary(Speech.REMOVE_PRODUCT_FAVORITES, Gestures.REMOVE, Output.REMOVE_PRODUCT_FAVORITES);
        fg.Complementary(Speech.SELECT, Gestures.SELECT, Output.SELECT);

        // Redundant
        fg.Redundancy(Speech.SCROLL_UP, Gestures.SCROLL_UP, Output.SCROLL_UP);
        fg.Redundancy(Speech.SCROLL_DOWN, Gestures.SCROLL_DOWN, Output.SCROLL_DOWN);
        fg.Redundancy(Speech.GO_BACK, Gestures.GO_BACK, Output.GO_BACK);
        fg.Redundancy(Speech.MAIN_PAGE, Gestures.MAIN_PAGE, Output.MAIN_PAGE);

        // Single Voice
        fg.Single(Speech.OPEN_WEBSITE, Output.OPEN_WEBSITE);
        fg.Single(Speech.SHOW_FAVORITES, Output.SHOW_FAVORITES);
        fg.Single(Speech.SHOW_CART, Output.SHOW_CART);
        fg.Single(Speech.ADD_TO_CART, Output.ADD_TO_CART);
        fg.Single(Speech.ADD_TO_FAVORITES, Output.ADD_TO_FAVORITES);
        fg.Single(Speech.SHOW_MORE, Output.SHOW_MORE);

        fg.Single(Speech.SEARCH_PRODUCT_CAMAS, Output.SEARCH_PRODUCT_CAMAS);
        fg.Single(Speech.SEARCH_PRODUCT_CADEIRAS, Output.SEARCH_PRODUCT_CADEIRAS);
        fg.Single(Speech.SEARCH_PRODUCT_ARMARIOS, Output.SEARCH_PRODUCT_ARMARIOS);
        fg.Single(Speech.SEARCH_PRODUCT_ESTANTES, Output.SEARCH_PRODUCT_ESTANTES);
        fg.Single(Speech.SEARCH_PRODUCT_SOFAS, Output.SEARCH_PRODUCT_SOFAS);
        fg.Single(Speech.SEARCH_PRODUCT_MESAS, Output.SEARCH_PRODUCT_MESAS);

        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_1, Output.SELECT_PRODUCT_BY_POSITION_1);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_2, Output.SELECT_PRODUCT_BY_POSITION_2);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_3, Output.SELECT_PRODUCT_BY_POSITION_3);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_4, Output.SELECT_PRODUCT_BY_POSITION_4);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_5, Output.SELECT_PRODUCT_BY_POSITION_5);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_6, Output.SELECT_PRODUCT_BY_POSITION_6);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_7, Output.SELECT_PRODUCT_BY_POSITION_7);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_8, Output.SELECT_PRODUCT_BY_POSITION_8);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_9, Output.SELECT_PRODUCT_BY_POSITION_9);
        fg.Single(Speech.SELECT_PRODUCT_BY_POSITION_10, Output.SELECT_PRODUCT_BY_POSITION_10);

        fg.Single(Speech.FINALIZE_ORDER, Output.FINALIZE_ORDER);

        fg.Single(Speech.AFFIRM, Output.AFFIRM);
        fg.Single(Speech.DENY, Output.DENY);

        // Single Gestures
        fg.Single(Gestures.CLOSE_WEB, Output.CLOSE_WEB);
        fg.Single(Gestures.GO_UP, Output.GO_UP);
        fg.Single(Gestures.GO_DOWN, Output.GO_DOWN);
        fg.Single(Gestures.GO_LEFT, Output.GO_LEFT);
        fg.Single(Gestures.GO_RIGHT, Output.GO_RIGHT);

        fg.Build("fusion.scxml");
    }
}