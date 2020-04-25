
// T15_37_16401_Abdullah_Elkady
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Stack;

public class T15_37_16401_Abdullah_Elkady {

  /*
   * Please update the file/class name, and the following comment
   */

  // T15_37_16401_Abdullah_Elkady

  static class CFG {

    // ===================================================================== //
    /*
     * The first&follow code in the following comment-block is taken from a 37-
     * student, credits to "Mohamed Ibrahim".
     */
    // ===================================================================== //

    final static Character EPSILON = 'e';
    final static String EPSILON_RULE = "e";

    /**
     * @param <T>
     * @param setA
     * @param setB
     * @return true if setA is a subset of setB
     */
    private static <T> boolean isSubset(LinkedHashSet<T> setA, LinkedHashSet<T> setB) {
      @SuppressWarnings({ "unchecked" })
      LinkedHashSet<T> temp = (LinkedHashSet<T>) setA.clone();
      temp.remove(EPSILON);
      return setB.containsAll(temp);
    }

    /**
     * Creates an instance of the CFG class. This should parse a string
     * representation of the grammar and set your internal CFG attributes
     *
     * @param grammar A string representation of a CFG
     */
    Map<Character, LinkedHashSet<String>> cfg;
    Map<Character, LinkedHashSet<Character>> first = new LinkedHashMap<>();
    Map<Character, LinkedHashSet<Character>> follow = new LinkedHashMap<>();
    LinkedHashSet<Character> sigma;

    public CFG(String input) {
      // input is in the form 'S,ScT,T;T,aSb,iaLb,e;L,SdL,S'
      this.cfg = new LinkedHashMap<>();
      this.sigma = new LinkedHashSet<Character>();
      for (Character c : input.toCharArray()) {
        if (isTerminal(c))
          this.sigma.add(c);
      }
      String[] rules = input.split(";");
      for (String rule : rules) {
        cfg.put(rule.charAt(0), new LinkedHashSet<String>(Arrays.asList(rule.substring(2, rule.length()).split(","))));
      }
      this.first = new LinkedHashMap<>();
      this.follow = new LinkedHashMap<>();
      this.First();
      this.Follow();
    }

    public String First() {
      for (Character variable : this.cfg.keySet()) {
        first.put(variable, new LinkedHashSet<Character>());
      }
      for (Character terminal : this.sigma) {
        first.put(terminal, new LinkedHashSet<Character>());
        first.get(terminal).add(terminal);
      }

      boolean change = true;
      while (change) {
        change = false;
        for (Character key : cfg.keySet()) {
          for (String production : cfg.get(key)) {
            if (hasAllEpsilon(production) && !first.get(key).contains(EPSILON)) {
              first.get(key).add(EPSILON);
              change = true;
            } else {
              for (int i = 0; i < production.toCharArray().length; i++) {
                if (i == 0 || hasAllEpsilon(production.substring(0, i))) {
                  char currentSymbol = production.charAt(i);
                  @SuppressWarnings("unchecked")
                  LinkedHashSet<Character> current = (LinkedHashSet<Character>) first.get(currentSymbol).clone();
                  current.remove(EPSILON);
                  if (!first.get(key).containsAll(current)) {
                    first.get(key).addAll(current);
                    change = true;
                  }
                }
              }
            }
          }
        }
      }
      String output = "";
      for (char variable : this.cfg.keySet()) {
        output += variable + ",";
        List<Character> sortedList = new ArrayList<>(first.get(variable));
        Collections.sort(sortedList);
        for (char c : sortedList) {
          output += c;
        }
        output += ";";
      }
      return output.substring(0, output.length() - 1);

    }

    public String Follow() {
      for (Character variable : this.cfg.keySet()) {
        follow.put(variable, new LinkedHashSet<Character>());
      }
      for (Character terminal : this.sigma) {
        follow.put(terminal, new LinkedHashSet<Character>());
      }
      follow.get('S').add('$');
      boolean change = true;
      while (change) {
        change = false;
        for (Character key : cfg.keySet()) {
          for (String production : cfg.get(key)) {
            for (int i = 0, n = production.length(); i < n; i++) {

              if (i == n - 1) {

                if (production.charAt(i) != EPSILON) {
                  if (!isSubset(follow.get(key), follow.get(production.charAt(i)))) {
                    @SuppressWarnings("unchecked")
                    LinkedHashSet<Character> current = (LinkedHashSet<Character>) follow.get(key).clone();
                    current.remove(EPSILON);
                    follow.get(production.charAt(i)).addAll(current);
                    change = true;
                  }
                }
              } else {
                if (!isSubset(first.get(production.charAt(i + 1)), follow.get(production.charAt(i)))) {

                  @SuppressWarnings("unchecked")
                  LinkedHashSet<Character> current = (LinkedHashSet<Character>) first.get(production.charAt(i + 1))
                      .clone();
                  current.remove(EPSILON);
                  follow.get(production.charAt(i)).addAll(current);
                  change = true;

                }

                if (first.get(production.charAt(i + 1)).contains(EPSILON) && i + 1 != n - 1) {

                  boolean flag = true;
                  int count = 1;

                  while (flag) {

                    if (!isSubset(first.get(production.charAt(i + 1 + count)), follow.get(production.charAt(i)))) {
                      @SuppressWarnings("unchecked")
                      LinkedHashSet<Character> current = (LinkedHashSet<Character>) first
                          .get(production.charAt(i + 1 + count)).clone();
                      current.remove(EPSILON);
                      follow.get(production.charAt(i)).addAll(current);
                      change = true;

                    }

                    if (i + 1 + count < n - 1 && first.get(production.charAt(i + 1 + count)).contains(EPSILON)) {

                      flag = true;
                      count++;
                    } else if (i + 1 + count == n - 1
                        && first.get(production.charAt(i + 1 + count)).contains(EPSILON)) {

                      if (!isSubset(follow.get(key), follow.get(production.charAt(i)))) {
                        @SuppressWarnings("unchecked")
                        LinkedHashSet<Character> current = (LinkedHashSet<Character>) follow.get(key).clone();
                        current.remove(EPSILON);
                        follow.get(production.charAt(i)).addAll(current);
                        change = true;

                      }

                      flag = false;
                    } else {

                      flag = false;
                    }
                  }
                } else if (first.get(production.charAt(i + 1)).contains(EPSILON) && i + 1 == n - 1) {

                  if (!isSubset(follow.get(key), follow.get(production.charAt(i)))) {
                    @SuppressWarnings("unchecked")
                    LinkedHashSet<Character> current = (LinkedHashSet<Character>) follow.get(key).clone();
                    current.remove(EPSILON);
                    follow.get(production.charAt(i)).addAll(current);
                    change = true;
                  }
                }
              }
            }
          }
        }
      }

      String output = "";
      for (char variable : this.cfg.keySet()) {
        output += variable + ",";
        List<Character> sortedList = new ArrayList<>(follow.get(variable));
        Collections.sort(sortedList);
        if (sortedList.contains('$')) {
          sortedList.remove(0);
          sortedList.add('$');
        }
        for (char c : sortedList) {
          output += c;
        }
        output += ";";
      }
      return output.substring(0, output.length() - 1);

    }

    private boolean hasAllEpsilon(String production) {
      for (Character symbol : production.toCharArray()) {
        if (first.get(symbol) != null && !first.get(symbol).contains(EPSILON))
          return false;

      }
      return true;
    }

    private boolean isTerminal(char symbol) {
      return !isVariable(symbol) && symbol != ';' && symbol != ',';
    }

    private boolean isVariable(char symbol) {
      return Character.isUpperCase(symbol);
    }

    private LinkedHashSet<Character> getFirst(String production) {
      LinkedHashSet<Character> output = new LinkedHashSet<Character>();
      if (hasAllEpsilon(production)) {
        output.add(EPSILON);
      }
      for (int i = 0; i < production.toCharArray().length; i++) {
        if (i == 0 || hasAllEpsilon(production.substring(0, i))) {
          char currentSymbol = production.charAt(i);
          @SuppressWarnings("unchecked")
          LinkedHashSet<Character> current = (LinkedHashSet<Character>) first.get(currentSymbol).clone();
          current.remove(EPSILON);
          output.addAll(current);
        }
      }
      return output;
    }

    // ===================================================================== //
    /*
     * End of first&follow code
     */
    // ===================================================================== //

    Map<String, String> currentTable = new LinkedHashMap<>();

    private String serializeTable() {
      List<Character> outputS = new ArrayList<Character>(this.sigma);
      Collections.sort(outputS);
      outputS.add('$');
      String output = "";

      for (int i = 0; i < this.cfg.keySet().size(); i++) {
        char k = (char) this.cfg.keySet().toArray()[i];
        for (int j = 0; j < outputS.size(); j++) {
          char t = outputS.get(j);
          if (!this.currentTable.containsKey(k + "" + t)) {
            continue;
          } else {
            output += (k + "," + t + "," + this.currentTable.get(k + "" + t) + ";");
          }
        }
      }
      return output.substring(0, output.length() - 1);
    }

    public String table() {
      for (int i = 0; i < this.cfg.keySet().size(); i++) {
        char c = (char) this.cfg.keySet().toArray()[i];
        for (int j = 0; j < this.cfg.get(c).size(); j++) {
          String p = (String) this.cfg.get(c).toArray()[j];
          LinkedHashSet<Character> returnedFirst = this.getFirst(p);
          for (int k = 0; k < returnedFirst.size(); k++) {
            char s = (char) returnedFirst.toArray()[k];
            if (s == 'e') {
              continue;
            } else {
              currentTable.put(c + "" + s, p);
            }
          }

          if (returnedFirst.contains('e')) {
            for (int k = 0; k < this.follow.get(c).size(); k++) {
              char s = (char) this.follow.get(c).toArray()[k];
              if (s == 'e') {
                continue;
              } else {
                currentTable.put(c + "" + s, p);
              }
            }
          }
        }
      }
      return this.serializeTable();
    }

    private String serializeParse(ArrayList<String> dList) {
      // To adapt to the required output, escape correctly.
      return dList.toString().replaceAll("[\\s\\[\\]]", "");
    }

    public String parse(String s) {
      int counter = 0;
      Stack<Character> myStack = new Stack<Character>();
      ArrayList<String> dList = new ArrayList<String>();
      myStack.push('$');
      myStack.push('S');
      dList.add("S");

      // Following the algorithm:
      boolean shouldStop = false;
      while (!shouldStop && !(myStack.peek() == '$' && counter == s.length())) {
        if (!isVariable(myStack.peek())) {
          boolean isError = !(counter < s.length() && s.charAt(counter) == myStack.peek());
          if (!isError) {
            myStack.pop();
            // Continue normally
            counter++;
          } else {
            dList.add("ERROR");
            // Mark it to stop execution! And add error
            shouldStop = true;
          }
        } else {
          char t = counter == s.length() ? '$' : s.charAt(counter);
          char c = myStack.pop();
          if (currentTable.containsKey(c + "" + t)) {
            String r = currentTable.get(c + "" + t);
            for (int j = r.length() - 1; j >= 0; j--) {
              if (r.charAt(j) != 'e') {
                myStack.push(r.charAt(j));
              }
            }
            dList.add(dList.get(dList.size() - 1).replaceFirst(c + "", r.replace("e", "")));
          } else {
            dList.add("ERROR");
            // Mark it to stop execution, and display the err
            shouldStop = true;
          }
        }
      }
      return this.serializeParse(dList);
    }
  }

  public static void main(String[] args) {

    /*
     * Please make sure that this EXACT code works. This means that the method and
     * class names are case sensitive
     */

    String grammar = "S,zToS,e;T,zTo,e";
    String input1 = "zzoozo";
    String input2 = "zoz";
    CFG g = new CFG(grammar);
    System.out.println(g.table());
    System.out.println(g.parse(input1));
    System.out.println(g.parse(input2));

  }
}