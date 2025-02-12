const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

async function scrapeProductDetails(url) {
    try {
        const headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'th,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.jib.co.th/'
        };

        const response = await axios.get(url, { headers });
        const $ = cheerio.load(response.data);
        
        const specifications = {};

        $('.panel-heading').each((index, element) => {
            const categoryName = $(element).text().trim();
            const categoryData = {};
            
            const nextPanelBody = $(element).next('.panel-body');
            nextPanelBody.find('.row.bor_top').each((i, row) => {
                const label = $(row).find('.quest').text().trim();
                const value = $(row).find('.answer').text().trim();
                
                if (label && value) {
                    categoryData[label] = value;
                }
            });

            if (Object.keys(categoryData).length > 0) {
                specifications[categoryName] = categoryData;
            }
        });

        return specifications;

    } catch (error) {
        console.error('เกิดข้อผิดพลาดในการดึงรายละเอียด:', error);
        return null;
    }
}

async function scrapeProducts(url) {
    try {
        const headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'th,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.jib.co.th/'
        };

        const response = await axios.get(url, { headers });
        const html = response.data;
        const $ = cheerio.load(html);

        const products = [];

        for (const element of $('.box_product')) {
            const brand = $(element).find('.brandspec').text().trim();
            const title = $(element).find('.titlespec').text().trim();
            const imgUrl = $(element).find('.img-responsive').attr('src');
            const price = $(element).find('span[style*="color: #ff3030"]')
                .text()
                .trim()
                .replace('.-', '');
            
            // ดึง URL รายละเอียดสินค้า
            const detailUrl = $(element).find('a.detail.btn.btndes').attr('href');
            
            // รอสักครู่ก่อนดึงข้อมูลรายละเอียด
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // ดึงข้อมูลรายละเอียดสินค้า
            const specifications = await scrapeProductDetails(detailUrl);

            products.push({
                brand,
                title,
                imgUrl: `https://www.jib.co.th${imgUrl}`,
                price,
                specifications
            });

            console.log(`ดึงข้อมูลสินค้า ${title} เรียบร้อยแล้ว`);
        }

        fs.writeFileSync(
            'vga.json', 
            JSON.stringify(products, null, 2), 
            'utf8'
        );

        console.log('บันทึกไฟล์ JSON เรียบร้อยแล้ว');
        return products;

    } catch (error) {
        console.error('เกิดข้อผิดพลาด:', error);
        return [];
    }
}

const url = 'https://www.jib.co.th/web/pcsetspec/load_product/vga';

scrapeProducts(url)
    .then(products => {
        console.log('จำนวนสินค้าที่พบ:', products.length);
    })
    .catch(error => {
        console.error('เกิดข้อผิดพลาดในการดึงข้อมูล:', error);
    });