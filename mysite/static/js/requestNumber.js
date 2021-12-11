const totalRequest = {
    data() {
        return {
            // suggestions: []
            totalRequest: 0
        }
    },
    mounted() {
        //get request
        //use results
        axios.get('/totalRequest/')
            .then(function (response) {
                // handle success
                myapp.totalRequest = response.data.totalRequest;
                console.log(myapp.totalRequest);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get('/totalRequest/')
            .then(function (response) {
                // handle success
                myapp.totalRequest = response.data.totalRequest;
                console.log(myapp.totalRequest);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

myapp = Vue.createApp(totalRequest).mount('#totalRequest')
