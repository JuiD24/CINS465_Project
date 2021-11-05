const ListRendering = {
    data() {
        return {
            // suggestions: []
            groupList: []
        }
    },
    mounted() {
        //get request
        //use results
        axios.get('/groupList/')
            .then(function (response) {
                // handle success
                myapp.groupList = response.data.groupLists;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get('/groupList/')
            .then(function (response) {
                // handle success
                myapp.groupList = response.data.groupLists;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

myapp = Vue.createApp(ListRendering).mount('#list-rendering')
