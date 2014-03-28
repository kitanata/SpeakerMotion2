SpeakerMotion.Models.Login = Backbone.Model.extend
    defaults:
        email: ""
        password: ""

    initialize: ->

    urlRoot: "/api/v1/user/login/"

    validation:
        email:
            required: true
            pattern: 'email'
            msg: "A valid email is required to sign in."
        password:
            required: true
            minLength: 8
            msg: "A password is required to sign in."
