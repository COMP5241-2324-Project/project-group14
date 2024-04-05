(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Sidebar Toggler
    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });


    // Progress Bar
    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});


    // Calender
    $('#calender').datetimepicker({
        inline: true,
        format: 'L'
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav : false
    });


    // Chart Global Color
    Chart.defaults.color = "#6C7293";
    Chart.defaults.borderColor = "#000000";

    document.querySelector('#ai-query').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
    
        const group_name = document.querySelector('#repository-name').value; // 获取输入的组名
        const group_owner = document.querySelector('#repository-owner').value;
        // const function_select = document.querySelector('#function-select').value;
        const data = {group_name, group_owner}
        console.log(data)
        fetch('/getInfoFromAi',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
            
        }) // 调用后端接口
        .then(response => response.json())
        .then(data => {
            document.querySelector('#ai-answer').value = data.answer;
        })
        .catch(error => console.error('Error:', error));
    });

    document.querySelector('#ai-query1').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
    
        const group_name1 = document.querySelector('#repository-name1').value; // 获取输入的组名
        const group_name2 = document.querySelector('#repository-name2').value; // 获取输入的组名
        const group_owner = document.querySelector('#repository-owner1').value;
        // const function_select = document.querySelector('#function-select').value;
        const data = {group_name1, group_name2, group_owner}
        console.log(data)
        fetch('/getGroupInfoFromAi',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
            
        }) // 调用后端接口
        .then(response => response.json())
        .then(data => {
            document.querySelector('#ai-answer1').value = data.answer;
        })
        .catch(error => console.error('Error:', error));
    });

    // Worldwide Sales Chart
    var ctx1 = $("#worldwide-sales").get(0).getContext("2d");
    var myChart1 = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: ["group1", "group2", "group3", "group4"],
            datasets: [{
                    label: "ISSUES",
                    data: [15, 30, 55, 65],
                    backgroundColor: "rgba(235, 22, 22, .7)"
                },
                {
                    label: "COMMENTS",
                    data: [8, 35, 40, 60],
                    backgroundColor: "rgba(235, 22, 22, .5)"
                },
                {
                    label: "CODE CHANGES",
                    data: [12, 25, 45, 55],
                    backgroundColor: "rgba(235, 22, 22, .3)"
                }
            ]
            },
        options: {
            responsive: true
        }
    });
    // 点击按钮 在mychart1上添加数据
    document.querySelector('#queryButton').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
    
        const group = document.querySelector('#floatingInput').value; // 获取输入的组名
    
        fetch(`/getGroupInfo?group=${group}`) // 调用后端接口
        .then(response => response.json())
        .then(data => {
            
            // 更新图表数据
            myChart1.data.labels.push(group);
            myChart1.data.datasets[0].data.push(data.issues);
            myChart1.data.datasets[1].data.push(data.comments);
            myChart1.data.datasets[2].data.push(data.codeChanges);
            myChart1.update();
        })
        .catch(error => console.error('Error:', error));
    });

    // Salse & Revenue Chart
    var ctx2 = $("#salse-revenue").get(0).getContext("2d");
    var myChart2 = new Chart(ctx2, {
        type: "line",
        data: {
            labels: ["26/02", "03/03", "10/03", "17/03", "24/03", "31/03", "07/04"],
            datasets: [
                {
                    label: "group 1",
                    data: [15, 30, 55, 45, 70, 65, 85],
                    backgroundColor: "rgba(235, 22, 22, .7)",
                    fill: true
                },
                {
                    label: "group 2",
                    data: [99, 135, 170, 130, 190, 180, 270],
                    backgroundColor: "rgba(235, 22, 22, .5)",
                    fill: true
                }
            ]
            },
        options: {
            responsive: true
        }
    });
    // 点击按钮 在mychart2上添加数据
    document.querySelector('#queryButton1').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
    
        const group = document.querySelector('#floatingInput1').value; // 获取输入的组名
    
        fetch(`/getGroupCommitFrequency?group=${group}`) // 调用后端接口
        .then(response => response.json())
        .then(data => {
            // 更新图表数据
            myChart2.data.datasets.push({
                label: data.group,
                data: data.commitFrequency,
                backgroundColor: "rgba(235, 22, 22, .3)",
                fill: true
            })
            myChart2.update();
        })
        .catch(error => console.error('Error:', error));
    });
    // Pie Chart
    var ctx5 = $("#pie-chart").get(0).getContext("2d");
    var myChart5 = new Chart(ctx5, {
        type: "pie",
        data: {
            labels: [],
            datasets: [{
                backgroundColor: [],
                data: []
            }]
        },
        options: {
            responsive: true
        }
    });
    // 点击按钮 在mychart2上添加数据
    document.querySelector('#queryButton2').addEventListener('click', function(event) {
        event.preventDefault(); // 阻止表单的默认提交行为
    
        const group = document.querySelector('#floatingInput2').value; // 获取输入的组名
    
        fetch(`/getGroupMemberContributor?group=${group}`) // 调用后端接口
        .then(response => response.json())
        .then(data => {
            // 更新图表数据
            myChart5.data.labels = data.labels;
            myChart5.data.datasets[0].backgroundColor = [
                "rgba(235, 22, 22, .7)",
                "rgba(235, 22, 22, .6)",
                "rgba(235, 22, 22, .5)",
                "rgba(235, 22, 22, .4)",
                "rgba(235, 22, 22, .3)"
            ];
            myChart5.data.datasets[0].data = data.memberContributor;
            myChart5.update();
        })
        .catch(error => console.error('Error:', error));
    });

    // Doughnut Chart
    var ctx6 = $("#doughnut-chart").get(0).getContext("2d");
    var myChart6 = new Chart(ctx6, {
        type: "doughnut",
        data: {
            labels: ["Italy", "France", "Spain", "USA", "Argentina"],
            datasets: [{
                backgroundColor: [
                    "rgba(235, 22, 22, .7)",
                    "rgba(235, 22, 22, .6)",
                    "rgba(235, 22, 22, .5)",
                    "rgba(235, 22, 22, .4)",
                    "rgba(235, 22, 22, .3)"
                ],
                data: [55, 49, 44, 24, 15]
            }]
        },
        options: {
            responsive: true
        }
    });

    // Single Line Chart
    var ctx3 = $("#line-chart").get(0).getContext("2d");
    var myChart3 = new Chart(ctx3, {
        type: "line",
        data: {
            labels: [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
            datasets: [{
                label: "Salse",
                fill: false,
                backgroundColor: "rgba(235, 22, 22, .7)",
                data: [7, 8, 8, 9, 9, 9, 10, 11, 14, 14, 15]
            }]
        },
        options: {
            responsive: true
        }
    });


    // Single Bar Chart
    var ctx4 = $("#bar-chart").get(0).getContext("2d");
    var myChart4 = new Chart(ctx4, {    
        type: "bar",
        data: {
            labels: ["student 1", "student 2", "student 3", "student 4", "student 5"],
            datasets: [{
                backgroundColor: [
                    "rgba(235, 22, 22, .7)",
                    "rgba(235, 22, 22, .6)",
                    "rgba(235, 22, 22, .5)",
                    "rgba(235, 22, 22, .4)",
                    "rgba(235, 22, 22, .3)"
                ],
                data: [55, 49, 44, 24, 15]
            }]
        },
        options: {
            responsive: true
        }
    });



    
})(jQuery);

