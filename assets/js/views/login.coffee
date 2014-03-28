SpeakerMotion.Views.Login = SpeakerMotion.Views.BaseView.extend
    className: "login-form"
    template: "#login-templ"

    events:
        "click #login-submit": "onLoginSubmit"

    initialize: (options) ->
        @alertTempl = Handlebars.compile($('#register-alert-templ').html())
        @listenTo(@model, "change", @render)

    context: ->
        email: @model.get 'email'
        password: @model.get 'password'

    afterRender: ->
        Backbone.Validation.bind this, 
            valid: (view, attr) =>
                @$el.find('#' + attr + '-error').text ''
                $.colorbox.resize()
            invalid: (view, attr, error) =>
                @$el.find('#' + attr + '-error').text '(' + error + ')'
                $.colorbox.resize()
        $.colorbox.resize()

    onLoginSubmit: ->
        @model.set
            email: @$el.find('#email').val()
            password: @$el.find('#password').val()

        if @model.isValid(true)
            @model.save null,
                success: =>
                    window.location = '/'
                error: (model, xhr, options) =>
                    error = JSON.parse(xhr.responseText)
                    if error.error == "account_disabled"
                        html = @alertTempl({error: "This account has been disabled. Please contact customer care for help."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
                    else if error.error == "auth_failed"
                        html = @alertTempl({error: "Your username or password is incorrect."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
