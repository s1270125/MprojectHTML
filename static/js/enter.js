var radio1 = new Vue({
    el: "#radio1",
    data: {
        flag: 0
    },
    methods: {
        Flag: function(fl){
            this.flag=fl
        }
    },
    delimiters:["[[","]]"]
})