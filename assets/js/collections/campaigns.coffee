SpeakerMotion.Collections.Campaigns = Backbone.Collection.extend
    model: SpeakerMotion.Models.Campaign

    url: "/api/v1/campaign/"

    parse: (response) ->
        response.objects
