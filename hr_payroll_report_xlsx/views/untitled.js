  console.log('here',lang_date_format)
                    if (lang_date_format == 'MM/DD/YYYY') {
                        console.log('111111111111111')
                        var text_split = text.split('/');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[1]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'DD/MM/YYYY') {
                        console.log('222222222222222')
                        var text_split = text.split('/');
                        var year = parseInt(text_split[2]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[0]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'YYYY/MM/DD') {
                        console.log('333333333333333333')
                        var text_split = text.split('/');
                        var year = parseInt(text_split[0]);
                        var month = parseInt(text_split[1]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    if (lang_date_format == 'MM/YYYY/DD') {
                        console.log('4444444444444444444')
                        var text_split = text.split('/');
                        var year = parseInt(text_split[1]);
                        var month = parseInt(text_split[0]);
                        var day = parseInt(text_split[2]);
                        var jd = cal_greg.toJD(year, month, day);
                        var date = cal_hijri.fromJD(jd);
                        var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                        var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                        $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    }
                    // 
                    // if (lang_date_format == 'DD/MMMM/YYYY') {
                        
                    //     var text_split = text.split('/');
                    //     console.log('555555555555555555555',text_split,origin_text._locale._abbr,text,)
                    //     var year = parseInt(text_split[2]);
                    //     var month = parseInt(text_split[1]);
                    //     var day = parseInt(text_split[0]);
                    //     if(origin_text._locale._abbr == 'en'){
                    //         console.log('uuuuuuuuuuuuuuuuuuuuuuuu',typeof(month),typeof(text))
                    //         var month=parseInt(moment(text).month(text_split[1]).format("M"));
                    //         const d = new Date(text);
                    //         console.log('yyyyyyyyyyyyyyyyyyyyyysssssssssssssssssss',month,typeof(month),d)
                    //     }
                    //     console.log('dddddddddddddddddddddddd',cal_greg,year,month,day)
                    //     var jd = cal_greg.toJD(d.getYear(), d.getMonth(), d.getDate());
                    //     console.log('jdjdjdjdjdjdjdjd',jd)
                    //     var date = cal_hijri.fromJD(jd);
                    //     console.log('fromJDfromJDfromJDfromJDfromJD',fromJD)
                    //     var m = (date.month() >= 10 ? date.month() : "0" + date.month());
                    //     var d = (date.day() >= 10 ? date.day() : "0" + date.day());
                    //     console.log('hijjjjjjjjjjjj',date,cal_hijri)
                    //     $(this.$input_hijri).val(cal_hijri.formatDate('M d, yyyy', date));
                    // }
                    // 