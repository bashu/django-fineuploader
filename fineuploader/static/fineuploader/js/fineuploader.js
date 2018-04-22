(function ($) {
    "use strict";
    function initFineUploader() {
        $(".fineuploader").each(function (i, element) {
            var form = $(element).closest("form");
            var container = document.getElementById($(element).attr("data-element"));

            var uploader = new qq.FineUploader({
                element: container,
                request: {
                    endpoint: this.getAttribute("data-request-endpoint"),
                    params: {
                        'csrfmiddlewaretoken': $(form).find("[name=csrfmiddlewaretoken]").val(),
                        'field_name': $(element).find("input[type=file]").attr("name"),
                        'content_type': this.getAttribute("data-ct"),
                        'object_id': this.getAttribute("data-oid")
                    }
                },
                session: {
                    endpoint: this.getAttribute("data-session-endpoint"),
                    params: {
                        'csrfmiddlewaretoken': $(form).find("[name=csrfmiddlewaretoken]").val(),
                        'field_name': $(element).find("input[type=file]").attr("name"),
                        'content_type': this.getAttribute("data-ct"),
                        'object_id': this.getAttribute("data-oid")
                    }
                },
                deleteFile: {
                    enabled: true,
                    method: "POST",
                    endpoint: this.getAttribute("data-delete-endpoint"),
                    params: {
                        'csrfmiddlewaretoken': $(form).find("[name=csrfmiddlewaretoken]").val(),
                        'content_type': this.getAttribute("data-ct"),
                        'object_id': this.getAttribute("data-oid")
                    }
                },
                multiple: true,
                validation: {
                    acceptFiles: $(element).find("input[type=file]").attr("accept"),
                    itemLimit: this.getAttribute("data-fileLimit"),
                    sizeLimit: this.getAttribute("data-sizeLimit")
                },
                retry: {
                    enableAuto: true // defaults to false
                },
                callbacks: {
                    onSubmitted: function (id, name) {
                    },
                    onSessionRequestComplete: function(response, success, xhr) {
                        if (!success) {
                            console.log(response);
                        }
                    },
                    onError: function(id, name, errorReason, xhr) {
                        alert(name + ' : ' + errorReason);
                    },
                    onComplete: function(id, name, responseJSON, xhr) {
                    }
                }
            });
        });
    }
    $(function () {
        initFineUploader();
    });

    $(document).bind('DOMNodeInserted', function(e) {
    });
}(jQuery || django.jQuery));
