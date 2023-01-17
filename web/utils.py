import time

after_content = \
    '''
                        </div>

                    </div>
                </div>
                <div class="clearer">&nbsp;</div>
            </div>
        </div>
    </div>

    <div id="footer-wrapper">

        <div class="center-wrapper">
    
            <div id="footer">
    
                <div class="left">
                    <a href="../">Home</a> <span class="text-separator">|</span> <a href="account">Wallet</a> <span class="text-separator">|</span> <a href="notarization">Notarization</a> <span class="text-separator">|</span> <a href="chain">Blockchain</a> <span class="text-separator">|</span> <a href="management">Management</a>
                </div>
    
                <div class="right">
                    <a href="#">Top ^</a>
                </div>
    
                <div class="clearer">&nbsp;</div>
    
            </div>
    
        </div>
    
    </div>
    
    <div id="bottom">
    
        <div class="center-wrapper">
    
            <div class="left">
                &copy; 2023 Blockchain-enabled Notarization Platform <span class="text-separator">|</span> <a href="https://www.gla.uestc.edu.cn/">Glasgow College, UESTC</a> <span class="text-separator">|</span> <a href="#">Final Year Project by Chenxiao Guo</a>
            </div>
    
            
    
            <div class="clearer">&nbsp;</div>
    
        </div>
    
    </div>

    </body>
    </html>

    '''
before_content = \
    '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" dir="ltr">

    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
        <meta name="description" content=""/>
        <meta name="keywords" content="" />
        <meta name="author" content="" />
        <link rel="stylesheet" type="text/css" href= "{{ url_for('static', filename = 'style.css') }}" media="screen" />
        <title>Website Template: Freshmade Software (demo)</title>
    </head>

    <body id="top">

    <div id="header-wrapper">
        <div id="header-wrapper-2">
            <div class="center-wrapper">

                <div id="header">

                    <div id="logo">
                        <h1 id="site-title"><a href="#">Blockchain-enabled <span>Notarization</span></a></h1>
                        <h2 id="site-slogan">Provide notarial services based on blockchain</h2>
                    </div>

                    <div id="help-wrapper">
                        <div id="help">

                            <a href="#">Contact us</a> <span class="text-separator">|</span> <a href="#">F.A.Q</a> <span class="text-separator">|</span> <a href="#">Sitemap</a>

                        </div>
                    </div>

                </div>

            </div>
        </div>
    </div>

    <div id="navigation-wrapper">
        <div id="navigation-wrapper-2">
            <div class="center-wrapper">

                <div id="navigation">

                    <ul class="tabbed">
                        <li><a href="../">Home</a></li>
                        <li><a href="account">Wallet</a></li>
                        <li><a href="notarization">Notarization</a></li>
                        <li class="current_page_item"><a href="chain">Blockchain</a></li>
                        <li><a href="management">Management</a></li>
                        <li><a href="empty_page.html">Empty Page</a></li>
                    </ul>

                    <div class="clearer">&nbsp;</div>

                </div>

            </div>
        </div>
    </div>

    <div id="content-wrapper">
        <div class="center-wrapper">
            <div class="content" id="content-two-columns">
                <div id="main-wrapper">
                    <div id="main">

    '''


def show_chain(length, hash, timestamp, tran):
    content = ''
    for n in range(1, length + 1):
        content += \
            '''
                        <div class="archive-post">
    
                            <div class="archive-post-date">
                                <div class="archive-post-day">Block</div>
                                <div class="archive-post-month">{}</div>
                            </div>
    
                            <div class="archive-post-title">
                                <h3><a href="http://127.0.0.1:5005/getBlock?index={}">{}</a></h3>
                                <div class="post-date">Mined at <a href="#">{}</a> | <a href="#">{} transactions</a></div>
                            </div>
    
                            <div class="clearer">&nbsp;</div>
    
                        </div>
    
                        <div class="archive-separator"></div>
            '''.format(n, n, '0x'+hash[n-1], timestamp[n-1], tran[n-1])
        content += '\n'

    with open("./templates/chain.html", "w") as f:
        f.write(before_content+content+after_content)


def show_block(block):
    if block:
        content =f'''<h2>Block Header</h2>

					<table class="data-table">
						<tr class="even">
							<td>Index</td>
							<td>{block['index']}</td>
						</tr>
						<tr>
							<td>Previous Hash</td>
							<td>{block['previous_hash']}</td>
						</tr>
						<tr class="even">
							<td>Proof</td>
							<td>{block['proof']}</td>
						</tr>
						<tr>
							<td>State Root</td>
							<td>{block['stateRoot']}</td>
						</tr>
						</tr>
						<tr>
							<td>Receipt Root</td>
							<td>{block['receiptsRoot']}</td>
						</tr>
						</tr>
						<tr>
							<td>Transaction Root</td>
							<td>{block['transactionRoot']}</td>
						</tr>
						</tr>
						<tr>
							<td>Timestamp</td>
							<td>{block['timestamp']}</td>
						</tr>
					</table>
					
					<div class="archive-separator"></div>
					
					<form method="get" action="/chain">
                        <div class="form-value"><input type="submit" class="button" value="Back to Chain" /></div>
                        <div class="clearer">&nbsp;</div>
                    </form>
					
					'''
    else:
        content = 'No Block'
    with open("./templates/block.html", "w") as f:
        f.write(before_content+str(content)+after_content)


def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


if __name__ == '__main__':
    timeStamp = 1673440348.7719
    print(timestamp2time(timeStamp))