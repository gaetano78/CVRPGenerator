# -*- coding: utf-8 -*-
"""STREAMLIT Dashboard - Generatore istanze Uchoa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nSozjnFgHEXC5bEHxJRrozDEAWylCCbs
"""

import streamlit as st
import random
import math
import matplotlib.pyplot as plt

# Imposta la configurazione della pagina
st.set_page_config(page_title="CVRP Generator", layout="wide")

# Aggiungi una barra del titolo
st.markdown(
    "<h1 style='text-align: center; color: navy;'>CVRP Generator</h1>",
    unsafe_allow_html=True,
)

# Aggiungi uno stile personalizzato per un aspetto professionale
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: navy;
        color: white;
    }
    .column-title {
        font-size: 24px;
        font-weight: bold;
        color: navy;
        margin-bottom: 10px;
        text-align: center;
    }
    .placeholder {
        background-color: #d3d3d3; /* Grigio scuro */
        border: 1px dashed #cccccc;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Crea tre colonne con rapporti di larghezza specifici
col1, col2, col3 = st.columns([1, 2, 1])

# Costanti
maxCoord = 1000  # Dimensione massima della griglia
decay = 40

# Funzione per calcolare la distanza euclidea tra due punti
def distance(x, y):
    return math.hypot(x[0] - y[0], x[1] - y[1])

# Funzione per generare il deposito
def generate_depot(rootPos, maxCoord):
    x_, y_ = (-1, -1)
    if rootPos == 1:
        x_ = random.randint(0, maxCoord)
        y_ = random.randint(0, maxCoord)
    elif rootPos == 2:
        x_ = y_ = int(maxCoord / 2.0)
    elif rootPos == 3:
        x_ = y_ = 0
    else:
        st.error("Depot Positioning out of range!")
        st.stop()
    depot = (x_, y_)
    return depot

# Funzione per generare le posizioni dei clienti
def generate_customer_positions(n, custPos, depot, nSeeds, maxCoord, decay):
    S = set()  # Insieme delle coordinate dei clienti
    seeds = []

    # Determina il numero di clienti posizionati casualmente
    if custPos == 3:
        nRandCust = int(n / 2.0)
    elif custPos == 2:
        nRandCust = 0
    elif custPos == 1:
        nRandCust = n
        nSeeds = 0
    else:
        st.error("Customer Positioning out of range!")
        st.stop()

    # Numero clienti clusterizzati
    nClustCust = n - nRandCust

    # Generazione dei clienti posizionati casualmente
    for _ in range(1, nRandCust + 1):
        x_ = random.randint(0, maxCoord)
        y_ = random.randint(0, maxCoord)
        while (x_, y_) in S or (x_, y_) == depot:
            x_ = random.randint(0, maxCoord)
            y_ = random.randint(0, maxCoord)
        S.add((x_, y_))
    nS = nRandCust

    # Generazione dei clienti clusterizzati
    if nClustCust > 0:
        if nClustCust < nSeeds:
            st.error("Too many seeds!")
            st.stop()

        # Generazione dei semi
        for _ in range(nSeeds):
            x_ = random.randint(0, maxCoord)
            y_ = random.randint(0, maxCoord)
            while (x_, y_) in S or (x_, y_) == depot:
                x_ = random.randint(0, maxCoord)
                y_ = random.randint(0, maxCoord)
            S.add((x_, y_))
            seeds.append((x_, y_))
        nS += nSeeds

        # Determina il seed con massimo peso
        maxWeight = 0.0
        for i, j in seeds:
            w_ij = 0.0
            for i_, j_ in seeds:
                w_ij += 2 ** (-distance((i, j), (i_, j_)) / decay)
            if w_ij > maxWeight:
                maxWeight = w_ij

        norm_factor = 1.0 / maxWeight

        # Generazione dei clienti rimanenti usando il metodo Accept-reject
        while nS < n:
            x_ = random.randint(0, maxCoord)
            y_ = random.randint(0, maxCoord)
            while (x_, y_) in S or (x_, y_) == depot:
                x_ = random.randint(0, maxCoord)
                y_ = random.randint(0, maxCoord)
            weight = 0.0
            for i_, j_ in seeds:
                weight += 2 ** (-distance((x_, y_), (i_, j_)) / decay)
            weight *= norm_factor
            rand = random.uniform(0, 1)
            if rand <= weight:
                S.add((x_, y_))
                nS += 1

    V = [depot] + list(S)  # Insieme dei vertici
    return V, seeds

# Funzione per generare le domande dei clienti
def generate_demands(V, demandType, r, n):
    demandMinValues = [1, 1, 5, 1, 50, 1, 51]
    demandMaxValues = [1, 10, 10, 100, 100, 50, 100]
    demandMin = demandMinValues[demandType - 1]
    demandMax = demandMaxValues[demandType - 1]
    demandMinEvenQuadrant = 51
    demandMaxEvenQuadrant = 100
    demandMinLarge = 50
    demandMaxLarge = 100
    largePerRoute = 1.5
    demandMinSmall = 1
    demandMaxSmall = 10

    D = []  # Demands
    sumDemands = 0
    maxDemand = 0

    for i in range(2, n + 2):
        j = int((demandMax - demandMin + 1) * random.uniform(0, 1) + demandMin)
        if demandType == 6:
            if (V[i - 1][0] < maxCoord / 2.0 and V[i - 1][1] < maxCoord / 2.0) or (
                V[i - 1][0] >= maxCoord / 2.0 and V[i - 1][1] >= maxCoord / 2.0
            ):
                j = int(
                    (demandMaxEvenQuadrant - demandMinEvenQuadrant + 1)
                    * random.uniform(0, 1)
                    + demandMinEvenQuadrant
                )
        if demandType == 7:
            if i < (n / r) * largePerRoute:
                j = int(
                    (demandMaxLarge - demandMinLarge + 1)
                    * random.uniform(0, 1)
                    + demandMinLarge
                )
            else:
                j = int(
                    (demandMaxSmall - demandMinSmall + 1)
                    * random.uniform(0, 1)
                    + demandMinSmall
                )
        D.append(j)
        if j > maxDemand:
            maxDemand = j
        sumDemands += j
    return D, sumDemands, maxDemand

# Funzione per calcolare la capacità
def compute_capacity(sumDemands, maxDemand, r, n):
    if sumDemands == n:
        capacity = math.floor(r)
    else:
        capacity = max(maxDemand, math.ceil(r * sumDemands / n))
    return capacity

# Funzione per generare il contenuto dell'istanza come stringa
def generate_instance_content(instanceName, n, capacity, V, D, demandType):
    content = ""
    content += "NAME : " + instanceName + "\n"
    content += "COMMENT : Generated as the XML100 dataset from the CVRPLIB\n"
    content += "TYPE : CVRP\n"
    content += "DIMENSION : " + str(n + 1) + "\n"
    content += "EDGE_WEIGHT_TYPE : EUC_2D\n"
    content += "CAPACITY : " + str(int(capacity)) + "\n"
    content += "NODE_COORD_SECTION\n"
    for i, v in enumerate(V):
        content += (
            "{:<4}".format(i + 1)
            + " "
            + "{:<4}".format(v[0])
            + " "
            + "{:<4}".format(v[1])
            + "\n"
        )
    content += "DEMAND_SECTION\n"
    if demandType != 6:
        random.shuffle(D)
    D = [0] + D
    for i, _ in enumerate(V):
        content += "{:<4}".format(i + 1) + " " + "{:<4}".format(D[i]) + "\n"
    content += "DEPOT_SECTION\n1\n-1\nEOF\n"
    return content

# Funzione per plottare l'istanza
def plot_instance(V, seeds):
    x = [v[0] for v in V]
    y = [v[1] for v in V]
    x_s = [v[0] for v in seeds]
    y_s = [v[1] for v in seeds]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(
        x[1:], y[1:], marker="o", color="blue", edgecolor="blue", s=40
    )
    if seeds:
        ax.scatter(
            x_s, y_s, marker="o", color="magenta", edgecolor="magenta", s=40
        )
    ax.scatter(
        [x[0]], [y[0]], marker="s", edgecolor="black", color="yellow", s=200
    )

    # Imposta i limiti degli assi con padding
    padding = maxCoord * 0.05  # 5% di padding
    ax.set_xlim(-padding, maxCoord + padding)
    ax.set_ylim(-padding, maxCoord + padding)

    # Rimuove le etichette e i tick degli assi
    ax.set_xticks([])
    ax.set_yticks([])

    return fig

# Colonna sinistra: Input dei parametri
with col1:
    st.markdown("<div class='column-title'>Settings</div>", unsafe_allow_html=True)
    n = st.number_input(
        "Numero di clienti (n)", min_value=1, max_value=1000, value=100
    )
    rootPos = st.selectbox(
        "Posizionamento del deposito (rootPos)",
        options=[1, 2, 3],
        index=0,
        format_func=lambda x: {1: "Random", 2: "Centro", 3: "Angolo in alto a sinistra"}[x],
    )
    custPos = st.selectbox(
        "Posizionamento dei clienti (custPos)",
        options=[1, 2, 3],
        index=0,
        format_func=lambda x: {1: "Random", 2: "Clusterizzato", 3: "Misto"}[x],
    )
    demandType = st.selectbox(
        "Tipo di distribuzione della domanda (demandType)",
        options=[1, 2, 3, 4, 5, 6, 7],
        index=0,
    )
    avgRouteSize = st.selectbox(
        "Dimensione media della rotta (avgRouteSize)",
        options=[1, 2, 3, 4, 5, 6],
        index=0,
    )
    instanceID = st.number_input(
        "ID dell'istanza (instanceID)", min_value=1, value=1
    )
    randSeed = st.number_input(
        "Seed casuale (randSeed)", min_value=0, value=1
    )

    # Aggiungi un pulsante per avviare l'elaborazione
    generate_button = st.button("Genera Istanza")

# Colonna centrale: Visualizza il plot o il placeholder
with col2:
    st.markdown("<div class='column-title'>Plot</div>", unsafe_allow_html=True)
    if generate_button:
        # Imposta il seed del generatore di numeri casuali
        random.seed(randSeed)
        nSeeds = random.randint(2, 6)
        # Genera il nome dell'istanza
        instanceName = (
            "XML"
            + str(n)
            + "_"
            + str(rootPos)
            + str(custPos)
            + str(demandType)
            + str(avgRouteSize)
            + "_"
            + format(instanceID, "02d")
        )
        # Genera l'istanza
        depot = generate_depot(rootPos, maxCoord)
        V, seeds = generate_customer_positions(n, custPos, depot, nSeeds, maxCoord, decay)
        # Calcola 'r' basato su avgRouteSize
        In = {1: (3, 5), 2: (5, 8), 3: (8, 12), 4: (12, 16), 5: (16, 25), 6: (25, 50)}
        if avgRouteSize > 6:
            st.error("Average route size out of range!")
            st.stop()
        r = random.uniform(In[avgRouteSize][0], In[avgRouteSize][1])
        D, sumDemands, maxDemand = generate_demands(V, demandType, r, n)
        capacity = compute_capacity(sumDemands, maxDemand, r, n)
        instance_content = generate_instance_content(instanceName, n, capacity, V, D, demandType)
        # Plot dell'istanza
        fig = plot_instance(V, seeds)
        st.pyplot(fig)
    else:
        # Mostra il placeholder
        st.markdown("<div class='placeholder'>Plot non disponibile</div>", unsafe_allow_html=True)

# Colonna destra: Visualizza il contenuto dell'istanza o il placeholder
with col3:
    st.markdown("<div class='column-title'>CVRP Instance</div>", unsafe_allow_html=True)
    if generate_button:
        # Visualizza il contenuto dell'istanza in un'area di testo scrollabile
        st.text_area("Istanza (.vrp format)", instance_content, height=400)
        # Fornisci un pulsante di download
        st.download_button(
            label="Scarica il file .vrp",
            data=instance_content,
            file_name=f"{instanceName}.vrp",
            mime="text/plain",
        )
    else:
        # Mostra il placeholder
        st.markdown("<div class='placeholder'>Istanza non disponibile</div>", unsafe_allow_html=True)

