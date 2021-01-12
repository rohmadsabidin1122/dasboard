odoo.define('custom_sale_dashboard.Dashboard', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var rpc = require('web.rpc');
var session = require('web.session');
var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;

var PosDashboard = AbstractAction.extend({
    template: 'PosDashboard',
    events: {
            'click #sales_orders': 'onclick_sales_order',
            'click #sales_product': 'onclick_product',
            // 'change #sales_teams': 'onclick_sales_teams',
            // 'change #sales_customers': 'onclick_top_product',
    },

    init: function(parent, context) {
        this._super(parent, context); 
        this.dashboards_templates = ['PosChart'];
        this.payment_details = [];
        this.top_salesperson = [];
        this.selling_product = [];
        this.total_sale = [];
    },

    start: function() {
        var self = this;
        rpc.query({
            model: "sale.order",
            method: "get_quotation",
          }).then(function (data) {
          self.$('.o_sale_quotation').append(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_order",
          }).then(function (data) {
          self.$('.o_sale_order').append(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_invoice",
          }).then(function (data) {
          self.$('.o_sale_invoice').append(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_teams",
          }).then(function (data) {
          self.$('.o_sale_team').append(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_top_customers",
          }).then(function (data) {
          self.$('.o_data_top_customer').append(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_top_sales",
          }).then(function (data) {
          self.$('.o_data_top_sales').append(data);
        })
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
            self.render_graphs();
            self.$el.parent().addClass('oe_background_grey');
        });
    },


    render_dashboards: function() {
        var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pos_dashboard').append(QWeb.render(template, {widget: self}));
            });
    },
      render_graphs: function(){
        var self = this;
        self.onclick_sales_teams();
        self.onclick_top_product();
        self.onclick_sales_order2();
        self.onclick_product2();

    },
//      get_emp_image_url: function(employee){
//        return window.location.origin + '/web/image?model=sale.order&field=image&id='+employee;
//    },

     onclick_sales_order:function(events){
        var option = $(events.target).val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "sale.order",
                method: "get_orders_chart",
                args: [option],
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "SALE ORDERS",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          if (window.myCharts1 != undefined)
          window.myCharts1.destroy();
          window.myCharts1 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },


    onclick_product:function(events){
        var option = $(events.target).val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_product_chart",
                args: [option],
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "PRODUCTS SOLD",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          if (window.myCharts2 != undefined)
          window.myCharts2.destroy();
          window.myCharts2 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: options
          });

        });
        },

    onclick_sales_teams:function(){
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_3");
            rpc.query({
                model: "sale.order",
                method: "get_teams_chart",
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "SALE TEAMS",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
         var chart = new Chart(ctx, {
            type: "horizontalBar",
            data: data,
            options: options
          });

        });
        },

    onclick_top_product:function(){
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_4");
            rpc.query({
                model: "sale.order",
                method: "get_top_product_list",
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "TOP PRODUCT",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },


    onclick_sales_order2:function(){
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "sale.order",
                method: "get_orders_chart_default",
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "TOP PRODUCT",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          window.myCharts1 = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },  
      
    onclick_product2:function(){
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_product_chart2",
            }).then(function (arrays) {
            console.log(arrays)
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "PRODUCTS SOLD",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#111",
                fontSize: 16
              }
            },
            scales: {
              yAxes: [{
                ticks: {
                  min: 0
                }
              }]
            }
          };

          //create Chart class object
          window.myCharts2 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: options
          });

        });
        },
});


core.action_registry.add('pos_dashboard', PosDashboard);

return PosDashboard;

});
