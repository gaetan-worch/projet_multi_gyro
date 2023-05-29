const a = document.getElementById('b');

new Chart(a, {
    type: 'line',
    data: {
    labels: [0, 1, 2, 3, 4, 5], //y
    datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        pointRadius : 0
    },]
    },
    options: {
    scales: {
        y: {
        beginAtZero: true
        }
    }
    }
});