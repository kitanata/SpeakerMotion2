SpeakerMotion.Views.Register = SpeakerMotion.Views.BaseView.extend
    className: "colorboxed-form"
    template: "#register-templ"

    events:
        "click #register-submit": "onRegisterSubmit"

    initialize: (options) ->
        @alertTempl = Handlebars.compile($('#alert-templ').html())
        @listenTo(@model, "change", @render)

    context: ->
        email: @model.get 'email'
        password: @model.get 'password'
        confirm: @model.get 'confirm'
        full_name: @model.get 'full_name'

    afterRender: ->
        Backbone.Validation.bind this, 
            valid: (view, attr) =>
                @$el.find('#' + attr + '-error').text ''
                $.colorbox.resize()
            invalid: (view, attr, error) =>
                @$el.find('#' + attr + '-error').text '(' + error + ')'
                $.colorbox.resize()
        $.colorbox.resize()

    onRegisterSubmit: ->
        @model.set
            email: @$el.find('#email').val()
            password: @$el.find('#password').val()
            confirm: @$el.find('#confirm').val()
            full_name: @$el.find('#full_name').val()

        if @model.isValid(true)
            @model.save null,
                success: =>
                    window.location = '/'
                error: (model, xhr, options) =>
                    error = JSON.parse(xhr.responseText)
                    if error.error == "email_taken"
                        html = @alertTempl({error: "An account with that email has already been registered."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
                    else if error.error == "password_match"
                        html = @alertTempl({error: "Your passwords do not match."})
                        $('#alert-area').show()
                        $('#alert-area').append html
                        $.colorbox.resize()
