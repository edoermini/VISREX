const data = [
    { id: 'start', label: 'Inizio' },
    { id: 'process1', label: 'Analisi' },
    { id: 'decision1', label: 'Esito Positivo?' },
    { id: 'process2', label: 'Elaborazione' },
    { id: 'end', label: 'Fine' },
];

const links = [
    { source: 'start', target: 'process1' },
    { source: 'process1', target: 'decision1' },
    { source: 'decision1', target: 'process2', type: 'yes' },
    { source: 'decision1', target: 'end', type: 'no' },
];

const svg = d3.select('svg');

const xScale = d3.scaleLinear().domain([0, data.length - 1]).range([50, 750]);

const nodes = svg.selectAll('g.node')
    .data(data)
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', (d, i) => `translate(${xScale(i)}, 200)`);

// Aggiungi cerchio per rappresentare i nodi
nodes.append('circle')
    .attr('r', 20)
    .style('fill', 'lightblue');

// Aggiungi testo per le etichette dei nodi
nodes.append('text')
    .attr('dy', 4)
    .attr('text-anchor', 'middle')
    .text(d => d.label);

// Aggiungi forme per i nodi decisionali (rettangoli con angoli arrotondati)
nodes.filter(d => d.id.includes('decision'))
    .append('rect')
    .attr('width', 40)
    .attr('height', 30)
    .attr('x', -20)
    .attr('y', -15)
    .attr('rx', 10)
    .attr('ry', 10)
    .style('fill', 'lightgreen');

const linkElements = svg.selectAll('path.link')
    .data(links)
    .enter()
    .append('path')
    .attr('class', 'link')
    .attr('d', d => {
        const sourceCoords = [xScale(data.findIndex(node => node.id === d.source)), 200];
        const targetCoords = [xScale(data.findIndex(node => node.id === d.target)), 200];

        if (d.type === 'yes') {
            // Se è un collegamento "yes", aggiungi una freccia all'estremità
            return `M${sourceCoords} Q${sourceCoords[0] + 40} ${200} ${targetCoords}M${targetCoords} L${targetCoords[0] - 10} ${190} L${targetCoords[0]} ${200} L${targetCoords[0] - 10} ${210} Z`;
        } else {
            // Altrimenti, un semplice collegamento
            return `M${sourceCoords} Q${sourceCoords[0] + 40} ${200} ${targetCoords}`;
        }
    })
    .style('stroke', 'black')
    .style('fill', 'none');