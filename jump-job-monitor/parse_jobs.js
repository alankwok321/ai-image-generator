const fs = require('fs');

const content = fs.readFileSync(process.argv[2], 'utf8');
// Simplified regex to capture title, link, school, date
const jobRegex = /<a class="title_name bold" href="([^"]+)">.*?<\/i>(.*?)<\/a>[\s\S]*?<a class="txt_14px" href="[^"]+">(.*?)<\/a>[\s\S]*?<span class="job-post-date text_jump_blue txt_12px">(.*?)<\/span>/g;

let match;
const jobs = [];
while ((match = jobRegex.exec(content)) !== null) {
    jobs.push({
        link: match[1],
        title: match[2].trim(),
        school: match[3].trim(),
        date: match[4].trim()
    });
}
console.log(JSON.stringify(jobs));
