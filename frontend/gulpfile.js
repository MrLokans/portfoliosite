var gulp = require('gulp');
var cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var inject = require('gulp-inject');
var minify = require('gulp-minify');
var less = require('gulp-less');
var ngConstant = require('gulp-ng-constant');
var rename = require('gulp-rename');
var watch = require('gulp-watch');
var webserver = require('gulp-webserver');
var debug = require('gulp-debug');
var gulpFilter = require('gulp-filter');

var del = require('del');

var mainBowerFiles = require('gulp-main-bower-files');
var bowerFiles = require('main-bower-files');

PATHS = {
  BUILD: 'build',
  THIRDPARTY: 'build/3rdparty'
}

// Cleans up build folder before the build start
gulp.task('clean:build', function(){
    return del.sync(PATHS.BUILD);
});
 

// Runs the development webserver
gulp.task('webserver', function() {
  gulp.src('build/')
    .pipe(webserver({
      port: 8090,
      livereload: true,
      directoryListing: false,
      open: true
    }));
});


gulp.task('concat:angular-dev',
          ['copy:assets', 'config:dev'],
          function(){
    return gulp
        .src(['js/app/app.js', 'build/app.constants.js', 'js/app/*.js', 'js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(gulp.dest('build/'));
});

gulp.task('concat:angular-prod',
          ['copy:assets', 'config:prod'],
          function(){
    return gulp
        .src(['js/app/app.js', 'build/app.constants.js', 'js/app/*.js', 'js/app/**/*.js'])
        .pipe(concat('angular.app.js'))
        .pipe(minify({
            ext:{
              source: '.js',
              min: '.min.js'
            }
          }))
        .pipe(gulp.dest('build/'));
});


gulp.task('config:dev', function(){
    return gulp.src('js/configs/dev.json')
          .pipe(ngConstant({
                "name": "andersblog.constants",
                "deps": [],
                "wrap": false,
                "wrapHeader": "(function(){",
                "wrapFooter": "});"
              }))
          .pipe(rename('app.constants.js'))
          .pipe(gulp.dest('build/'));
});

gulp.task('config:prod', function(){
    return gulp.src('js/configs/prod.json')
          .pipe(ngConstant({
                "name": "andersblog.constants",
                "deps": [],
                "wrap": false,
                "wrapHeader": "(function(){",
                "wrapFooter": "});"
              }))
          .pipe(rename('app.constants.js'))
          .pipe(gulp.dest('build/'))
});


// --------------- FILE COPYING -----------------
gulp.task('copy:bower-components', function(){
    return gulp.src(['./bower_components/**/*'])
        .pipe(gulp.dest('build/bower_components/'));
});

gulp.task('copy:angular', function(){
    // Copies angular js scripts
    return gulp.src(['js/app/**/*'])
        .pipe(gulp.dest('build/js/app/'));
});

gulp.task('copy:js', function(){
    // Copies custom javascript
    return gulp.src(['js/*.js'])
        .pipe(gulp.dest('build/js/'));
});

gulp.task('copy:vendor-css', function(){
    return gulp.src(['js/vendor/**/*.css'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:vendor-js', function(){
    return gulp.src(['js/vendor/**/*.js'])
        .pipe(gulp.dest('build/js/vendor/'));
});

gulp.task('copy:styles', function(){
    return gulp.src(['./css/*.css'])
        .pipe(gulp.dest('build/css'));
});

gulp.task('copy:images', function(){
    return gulp.src(['./img/**/*.png',
              './img/**/*/jpg',
              './img/**/*.svg'])
        .pipe(gulp.dest('build/img'));
});

gulp.task('copy:assets',
          ['copy:js', 'copy:vendor-js', 'copy:vendor-css', 
           'copy:styles', 'copy:images'],
          function(){});


// --------------- FILE INJECTION ---------------
gulp.task('inject:dev', ['concat:angular-dev'], function(){
    // Inject bower dependencies
    return gulp.src('./index.html')
        .pipe(inject(gulp.src('build/angular.app.js', {read: false}), {name: 'app'}))
        .pipe(debug())
        .pipe(inject(gulp.src(bowerFiles(), {read: false}), {name: 'bower'}))
        .pipe(gulp.dest('build'));
});

gulp.task('inject:prod',
          ['minify:3rdparty', 'concat:angular-prod'],
          function(){
    // Inject bower dependencies
    gulp.src(['build/3rdparty/**/*.min.js', 'build/3rdparty/**/*.min.css'])
      .pipe(debug());
    return gulp.src('./index.html')
        .pipe(inject(gulp.src(['build/3rdparty/**/*.min.js', 'build/3rdparty/**/*.min.css'], {read: false}, {name: 'bower'})))
        .pipe(inject(gulp.src(('build/angular.app.min.js'), {read: false}), {name: 'app'}))
        // .pipe(inject(gulp.src(bowerFiles(), {read: false}), {name: 'bower'}))
        .pipe(gulp.dest('build'));
});

gulp.task('build-dev',
          ['config:dev', 'inject:dev']);

gulp.task('build-prod',
          ['config:prod', 'inject:prod'],
          function(){});


gulp.task('minify:3rdparty', function(){
    var filterLESS = gulpFilter('**/*.less', { restore: true });
    var filterMinified = gulpFilter(['**/*.min.css', '**/*.min.js', '!**/*.min.min.*']);
    return gulp.src('./bower.json')
        .pipe(mainBowerFiles())
        .pipe(filterLESS)
        .pipe(less())
        .pipe(filterLESS.restore)
        .pipe(minify({
            ext:{
              source: '.js',
              min: '.min.js'
            }
          }))
        .pipe(minify({
            ext: {
              source: '.css',
              min: '.min.css'
            }
          }))
        .pipe(filterMinified)
        .pipe(debug())
        .pipe(gulp.dest('build/3rdparty'));
});

gulp.task('default',
          ['clean:build', 'build-dev', 'webserver'],
          function(){
    gulp.watch(['js/**', 'index.html', 'css/**'], function(event){
        gulp.run('copy:assets');
        gulp.run('build-dev');
    });
});

gulp.task('prod',
          ['clean:build', 'build-prod'],
          function(){});
