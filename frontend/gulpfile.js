var gulp = require('gulp');
var minify = require('gulp-minify');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var cleanCSS = require('gulp-clean-css');
var inject = require('gulp-inject');
var ngConstant = require('gulp-ng-constant');
var bowerFiles = require('main-bower-files');
 

gulp.task('concat-angular', function(){
    gulp.src(['./js/app/app.js', './js/app/*.js', './js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(gulp.dest('./js/dist/'));
});


gulp.task('config:dev', function(){
    gulp.src('js/configs/dev.json')
        .pipe(ngConstant({
              "name": "andersblog.constants",
              "deps": [],
              "wrap": false,
              "wrapHeader": "(function(){",
              "wrapFooter": "});"
            }))
        .pipe(rename('app.constants.js'))
        .pipe(gulp.dest('./js/app/'));
});

gulp.task('inject-bower', function(){
    gulp.src('./index.html')
        .pipe(inject(gulp.src(bowerFiles(), {read: false}), {name: 'bower'}))
        .pipe(gulp.dest('./build'));
});

gulp.task('default', function(){
    gulp.run('config:dev');
    gulp.run('concat-angular');

    gulp.watch('js/**', function(event){
        gulp.run('config:dev');
        gulp.run('concat-angular');
    });
});
