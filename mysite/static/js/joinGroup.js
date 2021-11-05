const joinGroupListRendering = {
    data() {
        return {
            // suggestions: []
            joinGroupList: []
        }
    },
    mounted() {
        //get request
        //use results
        axios.get('/joinGroupList/')
            .then(function (response) {
                // handle success
                myapp.joinGroupList = response.data.groupLists;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        setInterval(()=>{
            axios.get('/joinGroupList/')
            .then(function (response) {
                // handle success
                myapp.joinGroupList = response.data.groupLists;
                console.log(response);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
        }, 10000);

    }

}

myapp = Vue.createApp(joinGroupListRendering).mount('#JoinGrouplist-rendering')