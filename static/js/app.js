window.onload = function () {
    window.myBar = new Chart('myChart', {
        type: 'bar',
        options: {
            responsive: true,
            scales: {
                y: {
                    stacked: true,
                    grid: {
                        display: true,
                        color: 'rgba(255,99,132,0.2)'
                    }
                },
                x: {
                    grid: {
                        display: true
                    }
                }
            }
        },

        data: {
            labels: ['Janaury', 'February', 'March', 'April', 'May', 'June', 'Jule', 'August', 'September'],
            datasets: [{
                label: 'საშუალოდ მომხდარი ოჯახური ძალადობების რაოდენობა თვეების მიხედვით',
                backgroundColor: 'rgba(255,99,132,0.2)',
                borderColor: 'rgba(255,99,132,1)',
                borderWidth: 2,
                labelColor: '#a69296',
                hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                hoverBorderColor: 'rgba(255,99,132,1)',
                data: [65, 59, 20, 81, 56, 55, 40],
            }]
        }
    });


    window.myBar = new Chart('myChart1', {
        type: "line",
        data: {
            labels: [
                'იან.', 'თებ.', 'მარ.', 'აპრ.', 'მაი.', 'ივნ.', 'ივლ.',
                "აგვ.",
                "სექ.",
                "ოქტ.",
                "ნოე.",
                "დეკ."
            ],
            datasets: [
                {
                    label: "კაცები",
                    backgroundColor: "rgb(255, 99, 132)",
                    borderColor: "rgb(255, 99, 132)",
                    data: [0, 10, 5, 2, 20, 30, 17, 20, 22, 30, 28, 45]
                },
                {
                    label: "ქალები",
                    backgroundColor: "rgb(34,152,167)",
                    borderColor: "rgb(34,152,167)",
                    data: [0, 8, 15, 22, 10, 15, 18, 25, 26, 35, 37, 49]
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    stacked: true,
                    grid: {
                        display: true,
                        color: 'rgba(255,99,132,0.2)'
                    }
                },
                x: {
                    grid: {
                        display: true,
                        color: 'rgba(255,99,132,0.2)'
                    }
                }
            }
        },

    });
    window.myBar = new Chart('canvas', {
        type: "bar",
        data: {
            labels: ["ვაშლი", "ფორთოხალი", "ბანანი", "ჟოლო", "ანანასი"],
            datasets: [
                {
                    label: "ცუდი ხარისხის",
                    barPercentage: 0.7,
                    categoryPercentage: 0.7,
                    tension: 0.4,
                    borderWidth: 0,
                    borderRadius: 3,
                    borderSkipped: false,
                    backgroundColor: "rgba(6, 130, 247, 0.9)",
                    data: []
                },
                {
                    label: "კარგი ხარისხის",
                    barPercentage: 0.7,
                    categoryPercentage: 0.7,
                    tension: 0.4,
                    borderWidth: 0,
                    borderRadius: 3,
                    borderSkipped: false,
                    backgroundColor: "rgba(47, 209, 75, 0.9)",
                    data: [780, 620, 801, 407, 782]
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    labels: {
                        boxHeight: 10,
                        usePointStyle: true,
                        font: {
                            size: 14
                        }
                    },
                    position: "bottom",
                    align: "start"
                }
            },
            scales: {
                y: {
                    ticks: {
                        font: {
                            size: 16,
                            stepSize: 200
                        }
                    },
                    min: 0,
                    max: 1000,
                    stacked: false,
                    grid: {
                        display: true,
                        color: "rgba(255,99,132,0.2)"
                    }

                },
                x: {
                    ticks: {
                        font: {
                            size: 13
                        }
                    },
                    grid: {
                        display: true,
                        color: "rgba(255,99,132,0.2)",
                        borderWidth: 1,
                        borderDash: [10, 10]
                    }
                }
            }
        }
    });

    window.myBar = new Chart('canvas2', {
        type: "bar",
        data: {
            labels: [
                "0-10",
                "11-20",
                "21-30",
                "31-40",
                "41-50",
                "51-60",
                "61-70",
                "71-80",
                "80+"
            ],
            datasets: [
                {
                    label: "Q1",
                    barPercentage: 0.9,
                    categoryPercentage: 0.9,
                    tension: 0.4,
                    borderWidth: 0,
                    borderRadius: 3,
                    borderSkipped: false,
                    backgroundColor: "rgba(6, 130, 247, 0.9)",
                    data: [1, 1.5, 2, 3, 4.5, 7, 10.5, 14, 18]
                },
                {
                    label: "Q2",
                    barPercentage: 0.9,
                    categoryPercentage: 0.9,
                    tension: 0.4,
                    borderWidth: 0,
                    borderRadius: 3,
                    borderSkipped: false,
                    backgroundColor: "rgba(47, 209, 75, 0.9)",
                    data: [-1, -1.5, -2, -3, -4.5, -7, -10.5, -14, -18]
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: "y",
            plugins: {
                legend: {
                    labels: {
                        boxHeight: 10,
                        usePointStyle: true,
                        font: {
                            size: 16
                        }
                    },
                    position: "bottom",
                    align: "start"
                }
            },
            scales: {
                y: {
                    display: true,
                    ticks: {
                        font: {
                            size: 16
                        }
                    },
                    stacked: true,
                    grid: {
                        display: true,
                        color: "rgba(255,99,132,0.2)"
                    }
                },
                x: {
                    ticks: {
                        callback: function (t, i) {
                            return t < 0 ? Math.abs(t) : t;
                        },
                        font: {
                            size: 13
                        }
                    },
                    grid: {
                        display: true,
                        color: "rgba(255,99,132,0.2)",
                        borderWidth: 1,
                        borderDash: [10, 10]
                    }
                }
            }
        }
    });
};