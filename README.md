# congress_investigation
Deep Dive into Congressional Activity throughout the Drumpf Presidency:  

The purpose of this project is to investigate congressional activity and make that information freely available for the uninitiated.
This was accomplished by collecting every bill introduced by the House of Representatives across the Trump Presidency (115th and 116th congresses).
I then performed natural language processing on the bills to produce 15 categorical topic models using Latent Dirichlet Allocation (LDA) and grouped bills
by their majority assignment. Furthermore, I created a ScatterText for the set of bills in each topic in order to identify the different words
Republicans and Democrats use to talk about each topic.  

This all culminates in a Flask App which visualizes the information found through this project and provides the user with interactive pages created via Bokeh and
D3.js to make the information fully tangible and accessible.
