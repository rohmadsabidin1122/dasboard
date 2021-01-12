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
var i;
var text = [];
for (i = 0; i < 100; i++) {
  var a = Math.floor((Math.random() * 250));
  var b = Math.floor((Math.random() * 250));
  var c = Math.floor((Math.random() * 250));
  text.push("rgba("+a+", "+b+", "+c+", 1)");
}
var SaleDashboard = AbstractAction.extend({
    template: 'SaleDashboard',
    events: {
            'click #sales_orders': 'onclick_sales_order',
            'click #sales_product': 'onclick_product',
            'click #top_sales': 'onclick_top_sales',
            'click #top_customers': 'onclick_top_customers',
            'click #top_sales_product': 'onclick_top_product',
            'click #sales_team': 'onclick_sales_teams',
            // 'change #date_start': 'onclick_date_start',
            'click #button_action': 'onclick_date_end',
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
        var date1 = "";
        var date2 = "";

        rpc.query({
          model: "sale.order",
          method: "get_date_now",
        }).then(function (arrays) {
          document.getElementById('date_end').setAttribute("value", arrays[1]);
          document.getElementById('date_start').setAttribute("value", arrays[0]);

        })

        rpc.query({
            model: "sale.order",
            method: "get_quotation",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_quotation').html(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_order",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_order').html(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_invoice",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_invoice').html(data);
        })

        rpc.query({
            model: "sale.order",
            method: "get_teams",
          }).then(function (data) {
          self.$('.o_sale_team').append(data);
        })
        

        $('.dropdown-item.o_app.active').removeClass('active');
        $('.dropdown-menu.show').removeClass('show');
        $('.dropdown.show').removeClass('show');
        $(".full").attr("aria-expanded","False");
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
        self.onclick_top_product2();
        self.onclick_sales_order2();
        self.onclick_product2();
        self.onclick_sales_teams2();
        self.onclick_top_sales2();
        self.onclick_top_customers2();
    },
//      get_emp_image_url: function(employee){
//        return window.location.origin + '/web/image?model=sale.order&field=image&id='+employee;
//    },

     onclick_top_sales:function(events){
        // $("#date_start").val("");
        // $("#date_end").val("");
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        var self = this;
        rpc.query({
            model: "sale.order",
            method: "get_top_sales",
            args: [option,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_sales').html(data);
        })
     },

      onclick_top_sales2:function(events){
        var date1 = "";
        var date2 = "";
        var option = "top_sales_month";
        var self = this;
        rpc.query({
            model: "sale.order",
            method: "get_top_sales",
            args: [option,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_sales').html(data);
        })
     },

     onclick_top_customers:function(events){
        // $("#date_start").val("");
        // $("#date_end").val("");
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        var self = this;
        rpc.query({
            model: "sale.order",
            method: "get_top_customers",
            args: [option,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_customer').html(data);
        })
     },

      onclick_top_customers2:function(events){
        var date1 = "";
        var date2 = "";
        var option = "top_customers_month";
        var self = this;
        rpc.query({
            model: "sale.order",
            method: "get_top_customers",
            args: [option,date1,date2],
          }).then(function (data) {
          self.$('.o_data_top_customer').html(data);
        })
     },

    onclick_product:function(events){
        // $("#date_start").val("");
        // $("#date_end").val("");
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_product_chart",
                args: [option,date1,date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            // callbacks: { 
            //   label: function(tooltipItem, data) { 
            //     return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
            type: "doughnut",
            data: data,
            options: options
          });

        });
        },

    onclick_product2:function(events){
        var date1 = "";
        var date2 = "";
        var option = "pos_monthly_sales";
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_product_chart",
                args: [option,date1,date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            }, 
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            // callbacks: { 
            //   label: function(tooltipItem, data) { 
            //     return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
            type: "doughnut",
            data: data,
            options: options
          });

      });
    },

    onclick_sales_teams:function(events){
        // $("#date_start").val("");
        // $("#date_end").val("");
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_3");
            rpc.query({
                model: "sale.order",
                method: "get_teams_chart",
                args: [option, date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
          if (window.myCharts3 != undefined)
          window.myCharts3.destroy();
          window.myCharts3 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },

    onclick_sales_teams2:function(){
        var date1 = "";
        var date2 = "";
        var option = "pos_monthly_sales_team";
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_3");
            rpc.query({
                model: "sale.order",
                method: "get_teams_chart",
                args: [option, date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
          window.myCharts3 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });
        },

    onclick_top_product:function(events){
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        console.log('came monthly');
        var self = this;
        var ctx = self.$("#canvas_4");
            rpc.query({
                model: "sale.order",
                method: "get_top_product_list",
                args: [option, date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top",
                    // fontSize: 18,
                    // fontColor: "#111"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    // labels: {
                      // fontColor: "#111",
                      // fontSize: 16
                    // }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel', 
                   // callbacks: { 
                   //     label: function(tooltipItem, data) { 
                   //         return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

          // var options = {
          //   responsive: true,
          //   title: {
          //     display: true,
          //     position: "top",
          //     text: "",
          //     fontSize: 18,
          //     fontColor: "#111"
          //   },
          //   legend: {
          //     display: true,
          //     position: "bottom",
          //     font: {
          //         size: 18,
          //       }
          //   },
          //   tooltips: { 
          //   mode: 'label', 
          //   label: 'mylabel', 
          //   callbacks: { 
          //     label: function(tooltipItem, data) { 
          //       return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
          //   }, 
          //   scales: {
          //     yAxes: [{
          //       ticks: {
          //         min: 0
          //       }
          //     }]
          //   }
          // };

          //create Chart class object
          if (window.myCharts8 != undefined)
          window.myCharts8.destroy();
          window.myCharts8 = new Chart(ctx, {
//          var chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: options
          });

        });
        },

    onclick_top_product2:function(events){
        var date1 = "";
        var date2 = "";
        var option = "top_sales_product_month"
        console.log('came monthly');
        var self = this;
        var ctx = self.$("#canvas_4");
            rpc.query({
                model: "sale.order",
                method: "get_top_product_list",
                args: [option, date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          // var options = {
          //         responsive: true,
          //         title: {
          //           display: true,
          //           position: "top",
          //           // fontSize: 18,
          //           // fontColor: "#111"
          //         },
          //         legend: {
          //           display: true,
          //           position: "bottom",
          //           // labels: {
          //             // fontColor: "#111",
          //             // fontSize: 16
          //           // }
          //         },tooltips: { 
          //          mode: 'label', 
          //          label: 'mylabel', 
          //          callbacks: { 
          //              label: function(tooltipItem, data) { 
          //                  return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
          //         }, 
          //         scales: {
          //           yAxes: [{
          //             ticks: {
          //               min: 0
          //             }
          //           }]
          //         }
          //       };
          
          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "right",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            // callbacks: { 
            //   label: function(tooltipItem, data) { 
            //     return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
          //create Chart class object
          window.myCharts8 = new Chart(ctx, {
            type: "pie",
            data: data,
            options: options
          });

        });
        },


     onclick_sales_order:function(events){
        var date1 = "";
        var date2 = "";
        var option = $(events.target).val();
        console.log('came monthly')
        var self = this
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "sale.order",
                method: "get_orders_chart",
                args: [option,date1,date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
            type: "line",
            data: data,
            options: options
          });

        });
        },


      onclick_sales_order2:function(){
        var date1 = "";
        var date2 = "";
        console.log('came monthly')
        var self = this
        var option = "pos_monthly_sales";
        var ctx = self.$("#canvas_1");
            rpc.query({
                model: "sale.order",
                method: "get_orders_chart",
                args: [option,date1,date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
            type: "line",
            data: data,
            options: options
          });

        });
        },  


      onclick_date_start:function(){
          var date1 = $('#date_start').val();
          document.getElementById('date_end').setAttribute("min", date1);
          var date2 = $('#date_end').val();
          document.getElementById('date_start').setAttribute("max", date2);
          var option = "";

          // get top customer
          // $('#top_customers.active_button').removeClass('active_button');
          // var self = this;
          // rpc.query({
          //     model: "sale.order",
          //     method: "get_top_customers",
          //     args: [option,date1,date2],
          //   }).then(function (data) {
          //   self.$('.o_data_top_customer').html(data);
          // })


          // get top sales
          // $('#top_sales.active_button').removeClass('active_button');
          // var self = this;
          // rpc.query({
          //     model: "sale.order",
          //     method: "get_top_sales",
          //     args: [option,date1,date2],
          //   }).then(function (data) {
          //   self.$('.o_data_top_sales').html(data);
          // }) 

          // get sale order 
          // $('#sales_orders.active_button').removeClass('active_button');
          // console.log('came monthly');
          // var self = this;
          // var ctx1 = self.$("#canvas_1");
          //   rpc.query({
          //     model: "sale.order",
          //     method: "get_orders_chart",
          //     args: [option,date1,date2],
          //     }).then(function (arrays) {
          //       console.log(arrays)
          //       var data = {
          //       labels: arrays[1],
          //       datasets: [
          //       {
          //         label: arrays[2],
          //         data: arrays[0],
          //         backgroundColor: text,
          //         borderWidth: 1
          //       },
          //     ]
          //   };
          //   var options = {
          //     responsive: true,
          //     title: {
          //       display: true,
          //       position: "top",
                
          //       fontSize: 18,
          //       fontColor: "#111"
          //     },
          //     legend: {
          //     display: true,
          //     position: "bottom",
          //     labels: {
          //     fontColor: "#111",
          //     fontSize: 16
          //     }
          //   },
          //   tooltips: { 
          //     mode: 'label', 
          //     label: 'mylabel', 
          //     callbacks: { 
          //     label: function(tooltipItem, data) { 
          //       return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
          //     }, 
          //     scales: {
          //       yAxes: [{
          //         ticks: {
          //           min: 0
          //         }
          //       }]
          //     }
          //   };

            //create Chart class object
            // if (window.myCharts1 != undefined)
            // window.myCharts1.destroy();
            // window.myCharts1 = new Chart(ctx1, {
        },


        onclick_date_end:function(){
          var date1 = $('#date_start').val();
          document.getElementById('date_end').setAttribute("min", date1);
          var date2 = $('#date_end').val();
          document.getElementById('date_start').setAttribute("max", date2);
          var option = "";

          // to be invoiced
          rpc.query({
            model: "sale.order",
            method: "get_invoice",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_invoice').html(data);
          })

          // get quotation
          rpc.query({
            model: "sale.order",
            method: "get_quotation",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_quotation').html(data);
          })

          // sale orders
           rpc.query({
            model: "sale.order",
            method: "get_order",
            args: [date1, date2],
          }).then(function (data) {
          self.$('.o_sale_order').html(data);
        })

          // get top customer
          $('#top_customers.active_button').removeClass('active_button');
          var self = this;
          rpc.query({
              model: "sale.order",
              method: "get_top_customers",
              args: [option,date1,date2],
            }).then(function (data) {
            self.$('.o_data_top_customer').html(data);
          })

          // get top sales
          $('#top_sales.active_button').removeClass('active_button');
          var self = this;
          rpc.query({
              model: "sale.order",
              method: "get_top_sales",
              args: [option,date1,date2],
            }).then(function (data) {
            self.$('.o_data_top_sales').html(data);
          })   

          // get sale order
          if($('#sales_orders.active_button').val() != 'pos_monthly_sales'){
            $('#sales_orders.active_button').removeClass('active_button');
          }
          var option = $('#sales_orders.active_button').val()
          var self = this;
          var ctx1 = self.$("#canvas_1");
              rpc.query({
                  model: "sale.order",
                  method: "get_orders_chart",
                  args: [option,date1,date2],
              }).then(function (arrays) {
              console.log(arrays)
            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: arrays[2],
                  data: arrays[0],
                  backgroundColor: text,
                  borderWidth: 1
                },

              ]
            };

            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                
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
              tooltips: { 
              mode: 'label', 
              label: 'mylabel', 
              callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
            window.myCharts1 = new Chart(ctx1, {
  //          var chart = new Chart(ctx, {
              type: "line",
              data: data,
              options: options
            });

          });

      $('#sales_team.active_button').removeClass('active_button');
        var ctx2 = self.$("#canvas_3");
            rpc.query({
                model: "sale.order",
                method: "get_teams_chart",
                args: [option,date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
            responsive: true,
            title: {
              display: true,
              position: "top",
              text: "",
              fontSize: 18,
              fontColor: "#111"
            },
            legend: {
              display: true,
              position: "bottom",
              font: {
                  size: 18,
                }
            },
            tooltips: { 
            mode: 'label', 
            label: 'mylabel', 
            callbacks: { 
              label: function(tooltipItem, data) { 
                return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
          if (window.myCharts3 != undefined)
          window.myCharts3.destroy();
          window.myCharts3 = new Chart(ctx2, {
//          var chart = new Chart(ctx, {
            type: "bar",
            data: data,
            options: options
          });

        });


      $('#sales_product.active_button').removeClass('active_button');
      var ctx3 = self.$("#canvas_2");
            rpc.query({
                model: "sale.order",
                method: "get_product_chart",
                args: [option,date1,date2],
            }).then(function (arrays) {
                var data = {
                  labels: arrays[1],
                  datasets: [
                    {
                      label: arrays[2],
                      data: arrays[0],
                      backgroundColor: text,
                      borderWidth: 1
                    },

                  ]
                };

                var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top",
                    // fontSize: 18,
                    // fontColor: "#111"
                  },
                  legend: {
                    display: true,
                    position: "bottom",
                    // labels: {
                      // fontColor: "#111",
                      // fontSize: 16
                    // }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel', 
                   // callbacks: { 
                   //     label: function(tooltipItem, data) { 
                   //         return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
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
                window.myCharts2 = new Chart(ctx3, {
      //          var chart = new Chart(ctx, {
                  type: "doughnut",
                  data: data,
                  options: options
                });

              });


        $('#top_sales_product.active_button').removeClass('active_button');
        var ctx4 = self.$("#canvas_4");
            rpc.query({
                model: "sale.order",
                method: "get_top_product_list",
                args: [option, date1, date2],
            }).then(function (arrays) {
          var data = {
            labels: arrays[1],
            datasets: [
              {
                label: arrays[2],
                data: arrays[0],
                backgroundColor: text,
                borderWidth: 1
              },

            ]
          };

          var options = {
                  responsive: true,
                  title: {
                    display: true,
                    position: "top",
                    // fontSize: 18,
                    // fontColor: "#111"
                  },
                  legend: {
                    display: true,
                    position: "right",
                    // labels: {
                      // fontColor: "#111",
                      // fontSize: 16
                    // }
                  },tooltips: { 
                   mode: 'label', 
                   label: 'mylabel', 
                   // callbacks: { 
                       // label: function(tooltipItem, data) { 
                       //     return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
                  }, 
                  scales: {
                    yAxes: [{
                      ticks: {
                        min: 0
                      }
                    }]
                  }
                };

          // var options = {
          //   responsive: true,
          //   title: {
          //     display: true,
          //     position: "top",
          //     text: "",
          //     fontSize: 18,
          //     fontColor: "#111"
          //   },
          //   legend: {
          //     display: true,
          //     position: "bottom",
          //     font: {
          //         size: 18,
          //       }
          //   },
          //   tooltips: { 
          //   mode: 'label', 
          //   label: 'mylabel', 
          //   callbacks: { 
          //     label: function(tooltipItem, data) { 
          //       return tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }, }, 
          //   }, 
          //   scales: {
          //     yAxes: [{
          //       ticks: {
          //         min: 0
          //       }
          //     }]
          //   }
          // };

          //create Chart class object
          if (window.myCharts8 != undefined)
          window.myCharts8.destroy();
          window.myCharts8 = new Chart(ctx4, {
//          var chart = new Chart(ctx, {
            type: "pie",
            data: data,
            options: options
          });

        });

        },


});


core.action_registry.add('sale_dashboard', SaleDashboard);

return SaleDashboard;

}); 