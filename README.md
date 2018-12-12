# Messenger_chatbot

This project is completed by Aaron-Chang.


*   [Introduction](#intro)
*   [FSM Diagram](#diagram)
*   [Execution](#exec)
*   [Reference](#ref)
*  *  *
<h2 id="intro">Introduction</h2>
    This is an IR-based traditional chinese chatbot which can only be implemented on Messenger platfrom. The json file is from "中國信託(CTBC)", and I use BM25(Best Match25) to complete the task. Furthermore, the chatbot has 7 states where state0 is the initial state, and only state0 can perform BM25. As regards other states, state1 to state6 are simple FSM states which just accept certain strings.
<h2 id="diagram">FSM Diagram</h2>
![fsm] (./computation_theory_project/diagram.png)
<h3>To change state0 to state1</h3>
    *你好*
<h3>To change state0 to state2</h3>
    *你是誰*
<h3>To change state0 to state3</h3>
    *今天天氣很好*
<h3>To change state0 to state4</h3>
    *今天空氣很糟糕*
<h3>To change state4 to state5</h3>
    *你會建議使用哪種口罩*
<h3>To change state5 to state6</h3>
    *謝謝*
<h3>In state6</h3>
    *謝謝*
<h3>To return to state0</h3>
    *return*
<h2 id="exec">Execution</h2>
<h3>1. Set up an account in Facebook Developer and your page.</h3>
<h3>2. Download ngrok</h3>
<h3>3. run ngrok on port 8088:(Linux version)</h3>
    ./ngrook http 8088
<h3>4. run the chatbot</h3>
<h2 id="ref">Reference</h2>
*   [Facebook Developer](https://developers.facebook.com)
*   [Wikipedia tf-idf](https://en.wikipedia.org/wiki/Tf-idf)
*   [ngrok](https://ngrok.com)
*  *  *
