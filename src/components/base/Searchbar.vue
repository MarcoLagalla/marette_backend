<template>
    <div class="body" >
        <div class="body2" >
        <input id='search-btn' type='checkbox'/>
        <label for='search-btn'>Show search bar</label>
        <input id='search-bar' type='text' placeholder='Cerca...'/>
        </div>
    </div>

</template>


<script>

  export default {
    name: 'BaseSearchBar',


  }
</script>
<style scoped>
    .body2 {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 0 0 44px;
        min-height: 200px;
        width: 400px;
    }
    #btn--yp {
        box-sizing: content-box;
        position: fixed;
        z-index: 9;
        bottom: 1em;
        right: 1em;
        border: solid 1em transparent;
        width: 4.625em;
        height: 3.25em;
        background: url(https://s3-us-west-2.amazonaws.com/s.cdpn.io/2017/icon-yp.svg) 50%/cover content-box;
        font: 16px/ 1.25 trebuchet ms, sans-serif;
        text-indent: 200vw;
        text-shadow: none;
        filter: grayscale(1) drop-shadow(0 0 1px #e8e0e0);
        transition: .5s;
        white-space: nowrap;
    }
    #btn--yp:before {
        box-sizing: inherit;
        position: absolute;
        left: 0;
        bottom: 100%;
        margin: 1em -.5em;
        padding: .5em;
        width: 100%;
        border-radius: 5px;
        background: #e8e0e0;
        color: #000;
        text-align: center;
        text-decoration: none;
        text-indent: 0vw;
        white-space: normal;
        animation: float 1s ease-in-out infinite alternate;
        content: attr(data-txt);
    }
    #btn--yp:hover, #btn--yp:focus {
        outline: none;
        filter: grayscale(0) drop-shadow(0 0 1px crimson);
    }

    @keyframes float {
        to {
            transform: translateY(0.75em);
        }
    }
    *, :before, :after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        font: inherit;
    }

    html {
        overflow-x: hidden;
    }

    .body {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        width: 100%;
        min-height: 200px;

    }

    [id='search-btn'] {
        position: absolute;
        left: -100vw;
    }
    [id='search-btn'] ~ * {
        --i: var(--pos, 1);
        --j: calc(1 - var(--i))
    ;
    }
    [id='search-btn']:checked ~ * {
        --pos: 0 ;
    }

    [for='search-btn'] {
        order: 1;
        overflow: hidden;
        position: relative;
        z-index: 2;
        margin-left: -1.25em;
        width: 5em;
        height: 5em;
        border-radius: 50%;
        transform: translate(var(--pos, -10em)) rotate(45deg);
        background: hsl(calc(296 + var(--i)*269), calc(100% + var(--i)*2%), calc(65% + var(--i)*10%));
        text-indent: -100vw;
        transition: 0.65s ease-out;
        cursor: pointer;
    }
    [for='search-btn']:before, [for='search-btn']:after {
        position: absolute;
        top: 50%;
        left: 50%;
        margin: -0.8125em;
        width: 1.625em;
        height: 1.625em;
        transition: inherit;
        content: "";
    }
    [for='search-btn']:before {
        margin-top: -0.08125em;
        height: 0.203125em;
        transform-origin: 100% 0;
        transform: translate(var(--pos, 0.40625em)) scalex(calc(1 - var(--i)*.5));
        background: currentcolor;
    }
    [for='search-btn']:after {
        border: solid 0.203125em currentcolor;
        border-radius: calc(var(--i)*50%);
        transform: translate(var(--pos, -0.40625em)) scalex(calc(var(--j)*0.125 + var(--i)));
        box-shadow: inset 0 0 0 calc(var(--j)*0.8125em) currentcolor;
        transition-property: border-radius, transform, box-shadow;
        transition-timing-function: cubic-bezier(calc(var(--j)*.42), 0, calc(1 - var(--i)*.42), 1), cubic-bezier(calc(var(--i)*.42), 0, calc(1 - var(--j)*.42), 1);
    }

    [id='search-bar'] {
        margin-right: -1.25em;
        border: none;
        padding: 0 1em;
        width: 20em;
        height: 3.25em;
        border-radius: 3.25em;
        transform: translate(var(--pos, 10em));
        background: var(--lightgrey);
        --cp: inset(-2em var(--pos, 100%) -2em -2em);
        -webkit-clip-path: var(--cp);
        clip-path: var(--cp);
        color: darkslategrey;
        font: 1em century gothic, verdana, arial, sans-serif;
        transition: 0.65s;
    }
    [id='search-bar']::placeholder {
        opacity: .5;
        color: inherit;
        font-size: .875em;
        letter-spacing: 1px;
        text-shadow: 0 0 1px, 0 0 2px;
    }
    [id='search-bar']:focus {
        outline: none;
        box-shadow:  0 0 1em rgba(0, 0, 0, 0.2);
        background: var(--whitesmoke);
        color: #000;
    }

</style>