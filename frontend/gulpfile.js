var gulp = require('gulp');
var clean = require('gulp-clean');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var inject = require('gulp-inject');
var minify = require('gulp-minify');
var ngConstant = require('gulp-ng-constant');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var webserver = require('gulp-webserver');

var bowerFiles = require('main-bower-files');


gulp.task('clean:build', function(){
    // TODO: this causes errors due to async removal
    return gulp.src('./build/', {read: false}).pipe(clean());
});
 

gulp.task('webserver', function() {
  gulp.src('./build/')
    .pipe(webserver({
      port: 8090,
      livereload: true,
      directoryListing: false,
      open: true
    }));
});


gulp.task('concat:angular', function(){
    gulp.src(['./js/app/app.js', './build/app.constants.js', './js/app/*.js', './js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(gulp.dest('./build/'));
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
        .pipe(gulp.dest('./build/'));
});

gulp.task('copy:bower-components', function(){
    gulp.src(['./bower_components/**/*'])
        .pipe(gulp.dest('./build/bower_components/'));
});

gulp.task('copy:angular', function(){
    // Copies angular js scripts
    gulp.src(['./js/app/**/*'])
        .pipe(gulp.dest('./build/js/app/'));
})

gulp.task('inject:bower', function(){
    // Inject bower dependencies
    gulp.src('./index.html')
        .pipe(inject(gulp.src(bowerFiles(), {read: false}), {name: 'bower'}))
        .pipe(gulp.dest('./build'));
});

gulp.task('build-dev', function(){
    gulp.run('config:dev');
    gulp.run('concat:angular');
    gulp.run('inject:bower');
});
gulp.task('default', function(){
    // gulp.run('clean:build');
    gulp.run('copy:bower-components');

    gulp.run('build-dev')
    gulp.run('webserver');
    gulp.watch('js/**', function(event){
        gulp.run('build-dev')
    });
});
